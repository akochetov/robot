#!/usr/bin/python
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from gyro import MPU6050
from time import sleep, time

prev_time = 0
angle_x = 0
angle_y = 0

x_offset = 4
y_offset = -2
z_offset = 1

mpu = MPU6050(0x68)
while True:
	mpu.updateData()

	if prev_time == 0:
		prev_time = time()
		angle_x = mpu.getXrotation()
		angle_y = mpu.getYrotation()
	else:
		time_diff = time()-prev_time
		prev_time = time()
		angle_speed_x = (mpu.getXoutSc()+x_offset) * time_diff
		angle_speed_y = (mpu.getYoutSc()+y_offset) * time_diff
		angle_x -= angle_speed_x
		angle_y -= angle_speed_y

	#print "Time diff:", time_diff
	#print "X angle speed:",angle_speed_x
	#print "Y angle speed:",angle_speed_y
	print "X angle:", angle_x
	#print "Y angle:", angle_y

	#print "gyro data" 
	#print "---------"

	#print "gyro_xout: ", mpu.getXout(), " scaled: ", mpu.getXoutSc()
	#print "gyro_yout: ", mpu.getYout(), " scaled: ", mpu.getYoutSc()
	#print "gyro_zout: ", mpu.getZout(), " scaled: ", mpu.getZoutSc()

	print "x rotation: " , mpu.getXrotation()
	#print "y rotation: " , mpu.getYrotation()

	sleep(0.1)
	
