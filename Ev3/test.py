#!/usr/bin/env python3

from ev3dev2.motor import OUTPUT_B, OUTPUT_C, MoveTank, SpeedPercent
from ev3dev2.sensor.lego import GyroSensor

# Instantiate the MoveTank object
tank = MoveTank(OUTPUT_B, OUTPUT_C)

# Initialize the tank's gyro sensor
tank.gyro = GyroSensor()

# Calibrate the gyro to eliminate drift, and to initialize the current angle as 0
tank.gyro.reset()

# Pivot 30 degrees
tank.turn_degrees(
    speed=SpeedPercent(5),
    target_angle=180,
    sleep_time=0.01
)

tank.turn_degrees(
    speed=SpeedPercent(5),
    target_angle=-90,
    sleep_time=0.01
)

tank.turn_degrees(
    speed=SpeedPercent(5),
    target_angle=90,
    sleep_time=0.01
)
# import paho.mqtt.client as mqtt

# from ev3dev2.motor import LargeMotor, MoveSteering, OUTPUT_B, OUTPUT_C
# from ev3dev2.sensor import INPUT_2, INPUT_3, INPUT_4
# from ev3dev2.sensor.lego import ColorSensor

# motor_left = LargeMotor(OUTPUT_B)
# motor_right = LargeMotor(OUTPUT_C)
# # colour_left = ColorSensor(INPUT_2)
# # colour_center = ColorSensor(INPUT_3)
# # colour_right = ColorSensor(INPUT_4)
# # colour_left.mode = ColorSensor.MODE_COL_REFLECT
# # colour_center.mode = ColorSensor.MODE_COL_REFLECT
# # colour_right.mode = ColorSensor.MODE_COL_REFLECT

# motors = MoveSteering(OUTPUT_B, OUTPUT_C, motor_class=LargeMotor)

# def move_tank(power_left, power_right, value, _brake=False):
#     if power_left != 0:
#         motor_left.on_for_degrees(power_left,
#                                         value,
#                                         brake=_brake,
#                                         block=(power_right == 0))
#     if power_right != 0:
#         motor_right.on_for_degrees(power_right,
#                                         value,
#                                         brake=_brake,
#                                         block=True)

# def outside(val, mini, maxi):
#     return val < mini or val > maxi

# move_tank(-12, 12, 300)
# while outside(colour_center.value(), 70, 90) and outside(colour_left.value(), 20, 40) and outside(colour_right.value(), 20, 40):
#     print(colour_center.value(), colour_left.value(), colour_right.value())
#     motor_left.on(-12)
#     motor_right.on(12)

# print("Starting client!")
# client = mqtt.Client()
# # client.on_message = on_message

# client.connect("192.168.0.69", 1883, 60)
# client.loop_start()

# while True:
#     data = str(colour_left.value()) + str(colour_center.value()) + str(colour_right.value())
#     client.publish("my/topic", data)