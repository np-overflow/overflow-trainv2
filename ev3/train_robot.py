from ev3dev2.sound import Sound
from ev3dev2.motor import LargeMotor, MoveSteering, OUTPUT_B, OUTPUT_C, MoveTank, SpeedPercent
from ev3dev2.sensor import INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sensor.lego import ColorSensor
from ev3dev2.sensor.lego import GyroSensor

from direction import Direction

'''
blue green blue
25 25 25
30 35 30

blue red blue
30 65 30
30 65 30

blue yellow blue
30 83 30
30 80 30

white white white
95 95 95

'''

LINE_PT = 20
BACKGROUND_PT = 40
STATION_PT = 10

class TrainRobot:
    def __init__(self):
        self.motor_left = LargeMotor(OUTPUT_B)
        self.motor_right = LargeMotor(OUTPUT_C)
        self.motors = MoveSteering(OUTPUT_B, OUTPUT_C, motor_class=LargeMotor)

        self.tank = MoveTank(OUTPUT_B, OUTPUT_C)
        self.tank.gyro = GyroSensor()
        self.tank.gyro.reset()

        self.colour_left = ColorSensor(INPUT_2)
        self.colour_center = ColorSensor(INPUT_3)
        self.colour_right = ColorSensor(INPUT_4)

        self.sound = Sound()

        self.location = None
        self.direction = Direction.NONE

        self.colour_left.mode = ColorSensor.MODE_COL_REFLECT
        self.colour_center.mode = ColorSensor.MODE_COL_REFLECT
        self.colour_right.mode = ColorSensor.MODE_COL_REFLECT

    def line_trace(self, until, at_least = 10):
        count = 0
        while not until() or count < at_least:
            self.line_follower(14, 10)
            count += 1

    def line_follower(self, power1, power2):
        right_value = self.colour_right.value() > BACKGROUND_PT
        left_value = self.colour_left.value() > BACKGROUND_PT

        if left_value and right_value:
            pass

        elif left_value:
            self.motor_left.on(speed=power1)
            self.motor_right.on(speed=power2)
        
        elif right_value:
            self.motor_left.on(speed=power2)
            self.motor_right.on(speed=power1)

        else:
            self.motor_left.on(speed=power1)
            self.motor_right.on(speed=power1)

    def move_tank(self, power_left, power_right, value, _brake=False):
        if power_left != 0:
            self.motor_left.on_for_degrees(power_left,
                                           value,
                                           brake=_brake,
                                           block=(power_right == 0))
        if power_right != 0:
            self.motor_right.on_for_degrees(power_right,
                                           value,
                                           brake=_brake,
                                           block=True)

    def motor_break(self):
        self.motor_left.off()
        self.motor_right.off()

    def action_forward(self):
        print("action_forward")
        self.line_trace(self.at_station)
        self.speak('beep')
        self.move_tank(12, 12, 210)

    def action_turn_left(self):
        print("action_turn_left")
        self.tank.turn_degrees(
            speed=SpeedPercent(5),
            target_angle=-90,
            sleep_time=0.01
        )

    def action_turn_right(self):
        print("action_turn_right")
        self.tank.turn_degrees(
            speed=SpeedPercent(5),
            target_angle=90,
            sleep_time=0.01
        )

    def action_turn_back(self):
        print("action_turn_back")
        self.tank.turn_degrees(
            speed=SpeedPercent(5),
            target_angle=180,
            sleep_time=0.01
        )

    def at_station(self):
        return self.colour_center.value() < STATION_PT

    def speak(self, text):
        if text.lower() == 'beep':
            self.sound.beep()
            return
        self.sound.speak(text)
