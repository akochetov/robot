#!/usr/bin/python

from gyro import MPU6050
from time import sleep
      
mpu = MPU6050(0x68)
while True:
	mpu.updateData()

	print "gyro data"
	print "---------"

	print "gyro_xout: ", mpu.getXout(), " scaled: ", mpu.getXoutSc()
	print "gyro_yout: ", mpu.getYout(), " scaled: ", mpu.getYoutSc()
	print "gyro_zout: ", mpu.getZout(), " scaled: ", mpu.getZoutSc()

	print "x rotation: " , mpu.getXrotation()
	print "y rotation: " , mpu.getYrotation()

	sleep(0.1)
	
