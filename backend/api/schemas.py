from pydantic import BaseModel, EmailStr, model_validator
from typing import Optional, Literal, Self, List
from datetime import datetime

class SendCommandRequest(BaseModel):
    command: str
    value: Optional[int] = None

class SendCommandResponse(BaseModel):
    command: str
    value: Optional[int] = None
    command_success: bool

class ServoAngleRequest(BaseModel):
    angle: int

class ServoAngleRecordRequest(BaseModel):
    channel_0: int
    channel_1: int
    channel_2: int
    channel_3: int
    channel_4: int

class ServoAngleResponse(ServoAngleRecordRequest):
    pass
    