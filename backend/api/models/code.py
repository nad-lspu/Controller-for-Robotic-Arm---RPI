from ..mRPi import trixie_controller as tc

robot = tc.RoboticArm()
while True:
    robot.base.set_angle(90)
    tc.delay(1000)
    robot.lower_arm.set_angle(160)
    tc.delay(1000)
    robot.fore_arm(100)
    tc.delay(1000)