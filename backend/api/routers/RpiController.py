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

async def capture_live_camera_feed(websocket: WebSocket, is_rpi: bool, model: YOLO = YOLO('api/models/best.onnx')):
    if is_rpi:
        try:
            picam2 = Picamera2()
            picam2.start()
            while True:
                frame_rgb = picam2.capture_array()
                if model:
                    prediction = model(frame_rgb)[0]
                    for box in prediction.boxes:
                        xyxy = map(int, box.xyxy[0])
                        cls_id = int(box.cls[0])
                        label = model.names[cls_id]
                        frame_rgb = draw_boxes(frame_rgb, xyxy, label, color_sample[cls_id])
                frame_bgr = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2BGR)
                ret, buffer = cv2.imencode('.jpeg', frame_bgr)
                frame = buffer.tobytes()
                await websocket.send_bytes(frame)
                await asyncio.sleep(0.03)
        except WebSocketDisconnect:
            print('Camera Websocket Disconnected!')
        finally:
            picam2.close()
            print('Camera Hardware Released.')
    else:
        try:
            camera = cv2.VideoCapture(cv2.CAP_ANY)
            camera.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
            camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
            while True:
                success, frame = camera.read()
                if not success:
                    await asyncio.sleep(0.1)
                    continue
                if model:
                    prediction = model(frame)[0]
                    for box in prediction.boxes:
                        xyxy = map(int, box.xyxy[0])
                        cls_id = int(box.cls[0])
                        label = model.names[cls_id]
                        frame = draw_boxes(frame, xyxy, label, color_sample[cls_id])
                ret, buffer = cv2.imencode('.jpeg', frame)
                frame = buffer.tobytes()
                await websocket.send_bytes(frame)
                await asyncio.sleep(0.03)
        except WebSocketDisconnect:
            print('Camera Websocket Disconnected!')
        finally:
            camera.release()
            print('Camera Hardware Released.')
