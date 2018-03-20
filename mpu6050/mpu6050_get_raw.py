#!/usr/bin/python

from mpu6050 import *
import time


mpu = MPU6050()
mpu.initialize()

# Set calibration data
mpu.gyro_offs =  {'y': 312, 'x': -443, 'z': 216}
mpu.accel_offs =  {'y': 500, 'x': 200, 'z': 2100}

while True:
	gyro_data = mpu.get_gyro()
	accel_data = mpu.get_accel()

	print "Gyro: ", gyro_data
	print "Accel: ", accel_data
	print "Temperature: ",mpu.get_temp()

	time.sleep(0.1)
