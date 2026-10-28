from .database import Base
from sqlalchemy import Column, Integer

class ServoAngles(Base):
    __tablename__ = 'servo_angles'

    id = Column(Integer, primary_key=True, nullable=False)
    channel_0 = Column(Integer, nullable=False)
    channel_1 = Column(Integer, nullable=False)
    channel_2 = Column(Integer, nullable=False)
    channel_3 = Column(Integer, nullable=False)
    channel_4 = Column(Integer, nullable=False)