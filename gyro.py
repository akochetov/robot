#!/usr/bin/python

import smbus
import math
from time import sleep

class Bus():
        _address = None
        _bus = None

        _power_mgmt_1 = 0x6b
        _power_mgmt_2 = 0x6c

        def __init__(self,address):
                self._bus = smbus.SMBus(1) # or bus = smbus.SMBus(1) for Revision 2 boards
                self._address = address
                # Now wake the 6050 up as it starts in sleep mode
                self._bus.write_byte_data(self._address, self._power_mgmt_1, 0)

	def read_byte(self,adr):
    		return self._bus.read_byte_data(self._address, adr)

	def read_word(self,adr):
		high = self._bus.read_byte_data(self._address, adr)
		low = self._bus.read_byte_data(self._address, adr+1)
		val = (high << 8) + low
		return val

	def read_word_2c(self,adr):
		val = self.read_word(adr)
		if (val >= 0x8000):
        		return -((65535 - val) + 1)
		else:
			return val

	def dist(self,a,b):
		return math.sqrt((a*a)+(b*b))

	def get_y_rotation(self,x,y,z):
		radians = math.atan2(x, self.dist(y,z))
 		return -math.degrees(radians)

	def get_x_rotation(self,x,y,z):
    		radians = math.atan2(y, self.dist(x,z))
  		return math.degrees(radians)

class MPU6050(Bus):
	_accel_xout = 0
	_accel_yout = 0
	_accel_zout = 0

	_accel_xout_scaled = 0
	_accel_yout_scaled = 0
	_accel_zout_scaled = 0

	_gyro_xout = 0
	_gyro_yout = 0
	_gyro_zout = 0

	def updateData(self):
	        self._gyro_xout = self.read_word_2c(0x43)
		self._gyro_yout = self.read_word_2c(0x45)
		self._gyro_zout = self.read_word_2c(0x47)

        	self._accel_xout = self.read_word_2c(0x3b)
	        self._accel_yout = self.read_word_2c(0x3d)
        	self._accel_zout = self.read_word_2c(0x3f)

	        self._accel_xout_scaled = self._accel_xout / 16384.0
        	self._accel_yout_scaled = self._accel_yout / 16384.0
	        self._accel_zout_scaled = self._accel_zout / 16384.0

	def getXrotation(self):
		return self.get_x_rotation(self._accel_xout_scaled, self._accel_yout_scaled, self._accel_zout_scaled)

	def getYrotation(self):              
                return self.get_y_rotation(self._accel_xout_scaled, self._accel_yout_scaled, self._accel_zout_scaled)

	def getXout(self):
		return self._gyro_xout

        def getYout(self):
                return self._gyro_yout 

        def getZout(self):
                return self._gyro_zout

        def getXoutSc(self):
		return self._gyro_xout / 131

	def getYoutSc(self):
		return self._gyro_yout / 131

	def getZoutSc(self):
		return self._gyro_zout / 131

