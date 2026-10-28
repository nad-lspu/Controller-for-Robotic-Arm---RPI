from .database import SessionLocal
from . import models
from sqlalchemy.orm import Session
import random
import cv2

color_sample = [
    (12, 128, 255),   # Orange-ish
    (255, 0, 127),    # Pink
    (0, 255, 0),      # Green
    (255, 255, 0),    # Cyan
    (0, 165, 255)     # Blue-ish
]


def draw_boxes(image, box, label, color_sample):

    image_with_boxes = image.copy()

    xmin, ymin, xmax, ymax = map(int, box)

    # Draw bounding box
    cv2.rectangle(image_with_boxes, (xmin, ymin), (xmax, ymax), color_sample, 2)

    # Draw label text
    text = label
    text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1, 3)
    text_w, text_h = text_size

    # Adjust text position to prevent out-of-bounds
    ymin_text = max(ymin - text_h - 5, 0)

    # Background rectangle for text
    cv2.rectangle(image_with_boxes, (xmin, ymin_text-5), (xmin + text_w + 10, ymin), color_sample, -1)

    # Put text on the image with white color for better visibility
    cv2.putText(
        image_with_boxes,
        text,
        (xmin + 5, ymin - 5),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 0),  # White text
        2,
        cv2.LINE_AA,
    )

    return image_with_boxes

def initial_servo_angle_setup():
    db: Session = SessionLocal()
    try:
        servo_angles_query = db.query(models.ServoAngles).filter(models.ServoAngles.id == 1)

        if servo_angles_query.first():
            servo_angles_query.update({
                'channel_0': 90,
                'channel_1': 25,
                'channel_2': 0,
                'channel_3': 80,
                'channel_4': 90,
            }, synchronize_session=False)
            db.commit()
            return
        
        new_servo_angles = models.ServoAngles(
            channel_0=90,
            channel_1=25,
            channel_2=0,
            channel_3=80,
            channel_4=90,
            id=1,
        )

        db.add(new_servo_angles)
        db.commit()
        print('Initial Servo Angle Setup Complete')
    
    finally:
        db.close()