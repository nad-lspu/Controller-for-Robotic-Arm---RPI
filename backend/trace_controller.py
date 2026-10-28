
"""
TRACE robotic arm programming interface.

Exposes the existing TRIXIE controller library using the
module name expected by the TRACE Programming IDE.
"""

from api.mRPi.trixie_controller import (
    RoboticArm,
    Joint,
    Camera,
    UserInterface,
    delay,
)

__all__ = [
    "RoboticArm",
    "Joint",
    "Camera",
    "UserInterface",
    "delay",
]
