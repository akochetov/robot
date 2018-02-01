import RPi.GPIO as GPIO
from time import sleep
from datetime import  datetime

class PWMMotor:
	_pwm = None

	_pwm_freq = 500

	_enable_pin = 0
	_in1_pin = 0
	_in2_pin = 0

	def __init__(self,enable_pin,in1_pin,in2_pin,pwm_frequency=100):
		GPIO.setmode(GPIO.BCM)

		self._enable_pin = enable_pin
		self._in1_pin = in1_pin
		self._in2_pin = in2_pin
		self._pwm_freq = pwm_frequency

		self.setup()

	def setup(self):
		GPIO.setup(self._enable_pin,GPIO.OUT)	
		GPIO.setup(self._in1_pin,GPIO.OUT)
		GPIO.setup(self._in2_pin,GPIO.OUT)

		self._pwm = GPIO.PWM(self._enable_pin,self._pwm_freq)
                self._pwm.start(0)

	def rotate(self,clockwise,power=100):
		assert self._pwm is not None, "PWM was not yet setup. Call setup() first"
		print(str(datetime.now())+' Rotate motor: EN:'+str(self._enable_pin)+',IN1:'+str(self._in1_pin)+',IN2:'+str(self._in2_pin))

	        if clockwise:
        	        GPIO.output(self._in1_pin,GPIO.HIGH)
                	GPIO.output(self._in2_pin,GPIO.LOW)
	        else:
        	        GPIO.output(self._in1_pin,GPIO.LOW)
                	GPIO.output(self._in2_pin,GPIO.HIGH)

		self._pwm.ChangeDutyCycle(power)

	def stop(self):
		if self._pwm is not None:
			print(str(datetime.now())+' Stop motor: EN:'+str(self._enable_pin)+',IN1:'+str(self._in1_pin)+',IN2:'+str(self._in2_pin))
			GPIO.output(self._in1_pin, GPIO.LOW)
			GPIO.output(self._in2_pin, GPIO.LOW)
			self._pwm.ChangeDutyCycle(0)

	def cleanup(self):
		self.stop()
                if self._pwn is not None:
                        self._pwm.stop()
                        self._pwm = None


