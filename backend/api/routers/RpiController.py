from pydantic import BaseModel
from fastapi import APIRouter, HTTPException, status, Depends, WebSocket, WebSocketDisconnect, Response
from .. import schemas, models
from ..database import get_db
from ultralytics import YOLO
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from ..rpi_gpio_module import set_servo_angle
from ..utilities import draw_boxes, color_sample
from execution_manager import (
    start_test_program,
    stop_test_program,
    validate_demo_code,
    execute_demo_code,
    get_test_program_output,
)
import cv2
import platform
import asyncio

if platform.system() != 'Windows' and platform.system() != 'Darwin':
    from picamera2 import Picamera2 # type: ignore

router = APIRouter(prefix='/gpio', tags=['gpio'])

@router.get('/servo-angle', response_model=schemas.ServoAngleResponse)
def get_servo_angles(db: Session = Depends(get_db)):
    servo_angles =  db.query(models.ServoAngles).filter(models.ServoAngles.id == 1).first()

    if not servo_angles:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Servo Angle Data is not Found.'
        )
    
    return servo_angles

@router.post('/servo-angle', response_model=schemas.ServoAngleResponse)
def record_servo_angles(servo_angles: schemas.ServoAngleRecordRequest, db: Session = Depends(get_db)):
    servo_angles = models.ServoAngles(**servo_angles.model_dump(), id=1)

    try:
        db.add(servo_angles)
        db.commit()
        db.refresh(servo_angles)
        return servo_angles
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail='Servo Angle Record already Exists.'
        )
    
@router.websocket('/ws-servo')
async def servo_websocket_endpoint(websocket: WebSocket, db: Session = Depends(get_db)):
    await websocket.accept()
    print('Servo Websocket Connected!')
    try:
        while True:
            data = await websocket.receive_json()
            set_servo_angle(data['angle'], data['servo_channel'])
            update_servo_angles(db, data)
    except WebSocketDisconnect:
        print('Servo Websocket Disconnected!')

@router.websocket('/cam')
async def stream_camera(websocket: WebSocket):
    await websocket.accept()
    print('Camera Websocket Connected!')
    await capture_live_camera_feed(
        websocket, 
        is_rpi= (platform.system() != 'Windows' and platform.system() != 'Darwin')
    )


@router.post('/run_code')
def run_code():
    return start_test_program()


@router.post('/terminate_code')
def terminate_code():
    return stop_test_program()

class CodeValidationRequest(BaseModel):
    code: str
    
@router.get('/program_output')
def program_output():
    return get_test_program_output()

@router.post('/validate_code')
def validate_code(request: CodeValidationRequest):
    return validate_demo_code(request.code)

@router.post('/execute_demo_code')
def execute_demo(request: CodeValidationRequest):
    return execute_demo_code(request.code)

def update_servo_angles(db: Session, data: dict):
    channel = f"channel_{data['servo_channel']}"
    servo_angle_query = db.query(models.ServoAngles).filter(models.ServoAngles.id == 1)
    
    if not servo_angle_query.first():
        print('ERROR: Servo Angle Storage Not Found.')

    servo_angle_query.update({channel: data['angle']}, synchronize_session=False)
    db.commit()

# Only one client may own the camera at a time. A new connection preempts the old one.
_camera_lock = asyncio.Lock()
_active_stop_event: asyncio.Event | None = None


def _annotate(frame_bgr, model, rgb: bool):
    """Run detection and JPEG-encode. Blocking; call via asyncio.to_thread."""
    if model:
        prediction = model(frame_bgr)[0]
        for box in prediction.boxes:
            xyxy = map(int, box.xyxy[0])
            cls_id = int(box.cls[0])
            label = model.names[cls_id]
            frame_bgr = draw_boxes(frame_bgr, xyxy, label, color_sample[cls_id])
    if rgb:
        frame_bgr = cv2.cvtColor(frame_bgr, cv2.COLOR_RGB2BGR)
    ok, buffer = cv2.imencode('.jpeg', frame_bgr)
    return buffer.tobytes() if ok else None


async def _watch_disconnect(websocket: WebSocket, stop: asyncio.Event):
    """The stream loop never reads from the socket, so without this it would
    not notice the client leaving and would hold the camera forever."""
    try:
        while True:
            msg = await websocket.receive()
            if msg['type'] == 'websocket.disconnect':
                break
    except Exception:
        pass
    finally:
        stop.set()


async def capture_live_camera_feed(websocket: WebSocket, is_rpi: bool, model: YOLO = YOLO('api/models/best.onnx')):
    global _active_stop_event

    # Ask any previous stream to stop, then wait until it has released the camera.
    if _active_stop_event is not None:
        _active_stop_event.set()

    async with _camera_lock:
        stop = asyncio.Event()
        _active_stop_event = stop
        watcher = asyncio.create_task(_watch_disconnect(websocket, stop))
        camera = None
        picam2 = None
        try:
            if is_rpi:
                def open_cam():
                    cam = Picamera2()
                    cam.start()
                    return cam
                picam2 = await asyncio.to_thread(open_cam)
                grab = lambda: picam2.capture_array()
            else:
                def open_cam():
                    cam = cv2.VideoCapture(cv2.CAP_ANY)
                    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
                    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
                    return cam
                camera = await asyncio.to_thread(open_cam)
                if not camera.isOpened():
                    print('Camera could not be opened.')
                    await websocket.close(code=1011)
                    return

                def grab():
                    ok, f = camera.read()
                    return f if ok else None

            while not stop.is_set():
                frame = await asyncio.to_thread(grab)
                if frame is None:
                    await asyncio.sleep(0.1)
                    continue
                jpeg = await asyncio.to_thread(_annotate, frame, model, is_rpi)
                if jpeg is None or stop.is_set():
                    continue
                await websocket.send_bytes(jpeg)
                await asyncio.sleep(0.03)
        except (WebSocketDisconnect, RuntimeError):
            print('Camera Websocket Disconnected!')
        except Exception as e:
            print(f'Camera stream error: {e!r}')
        finally:
            watcher.cancel()
            if picam2 is not None:
                picam2.close()
            if camera is not None:
                camera.release()
            if _active_stop_event is stop:
                _active_stop_event = None
            print('Camera Hardware Released.')
