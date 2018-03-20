#!/usr/bin/python
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

#from gyro import MPU6050
from mpu6050 import MPU6050
from time import sleep, time

import os

prev_time = 0
angle_x = 0
angle_y = 0

x_offset = 1.2
y_offset = 0
z_offset = 0

mpu = MPU6050(0x68)
mpu.gyro_offs = {"y":312,"x":-443,"z":216}

#mpu.set_accel_range(0x18)
while True:
	data = mpu.get_all_data()
	time_diff = 0
	angle_speed_x = 0
	angle_speed_y = 0

	if prev_time == 0:
		prev_time = time()
		angle_x = data['accel_rotation']['x']
		angle_y = data['accel_rotation']['y']
	else:
		time_diff = time()-prev_time
		prev_time = time()
		angle_speed_x = (data['gyro']['x']*x_offset) * time_diff
		angle_speed_y = (data['gyro']['y']*y_offset) * time_diff
		angle_x = 0.98*(angle_speed_x+angle_x)+0.02*data['accel_rotation']['x']
		angle_y = 0.98*(angle_speed_y+angle_y)+0.02*data['accel_rotation']['y']

	os.system('clear')
	print "complimentary filter data"
	print "---------"
	print "time diff:", time_diff
	print "x angle speed:",angle_speed_x
	print "y angle speed:",angle_speed_y
	print "x angle:", angle_x
	print "y angle:", angle_y

	print "gyro/accel data" 
	print "---------"

	print "gyro_xout: ", data['gyro']['x']
	print "gyro_yout: ", data['gyro']['y']
	print "gyro_zout: ", data['gyro']['z']

	print "x rotation: " , data['accel_rotation']['x']
	print "y rotation: " , data['accel_rotation']['y']

	#sleep(0.1)
	
