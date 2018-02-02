from config import Cfg	#config json
import RPi.GPIO as GPIO
from motor import PWMMotor
from gyro import MPU6050
from time import sleep

pins = Cfg().get('left_motor')
lmotor = PWMMotor(pins['EN'], pins['IN1'], pins['IN2'])
pins = Cfg().get('right_motor')
rmotor = PWMMotor(pins['EN'], pins['IN1'], pins['IN2'])

power = 25

led = Cfg().get('ctrl_led')
GPIO.setup(led,GPIO.OUT)

while True:
	#turn led on
	GPIO.output(led,GPIO.HIGH)

	#test left motor 
	lmotor.rotate(True,power)
	sleep(1)
	lmotor.stop()

        GPIO.output(led,GPIO.LOW)

	lmotor.rotate(False,power)
	sleep(1)
	lmotor.stop()

        GPIO.output(led,GPIO.HIGH)

	#test right motor
	rmotor.rotate(True,power)
	sleep(1)
	rmotor.stop()

        GPIO.output(led,GPIO.LOW)

	rmotor.rotate(False,power)
	sleep(1)
	rmotor.stop()

        GPIO.output(led,GPIO.HIGH)

	#test both motors
	lmotor.rotate(False,power)
	rmotor.rotate(False,power)
	sleep(2)
	lmotor.stop()
	rmotor.stop()

        GPIO.output(led,GPIO.LOW)

	lmotor.rotate(True,power)
	rmotor.rotate(True,power)
	sleep(2)
	lmotor.stop()
	rmotor.stop()

        GPIO.output(led,GPIO.LOW)

	sleep(5)

lmotor.cleanup()
rmotor.cleanup()

GPIO.output(led,GPIO.LOW)

GPIO.cleanup()
