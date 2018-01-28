from config import Cfg	#config json
import RPi.GPIO as GPIO
from time import sleep
from datetime import  datetime

left_pwm = None
right_pwm = None

pwm_power = 50
pwm_freq = 500

GPIO.setmode(GPIO.BCM)

def pin(p):
	GPIO.setup(p,GPIO.OUT)
   	return p

def rotate(clockwise,en,in1,in2,pwm = None):
	print(str(datetime.now())+' Rotate motor: EN:'+str(en)+',IN1:'+str(in1)+',IN2:'+str(in2))

        if clockwise:
                GPIO.output(in1,GPIO.HIGH)
                GPIO.output(in2,GPIO.LOW)
        else:
                GPIO.output(in1,GPIO.LOW)
                GPIO.output(in2,GPIO.HIGH)

	#GPIO.output(en, GPIO.HIGH)
	if pwm is None:
		pwm = GPIO.PWM(en,pwm_freq)
		pwm.start(0)
	pwm.ChangeDutyCycle(pwm_power)
	return pwm

def stop(en,in1,in2,pwm):
	print(str(datetime.now())+' Stop motor: EN:'+str(en)+',IN1:'+str(in1)+',IN2:'+str(in2))

	#GPIO.output(in1, GPIO.LOW)
	#GPIO.output(in2, GPIO.LOW)
	#GPIO.output(en, GPIO.LOW)
	pwm.ChangeDutyCycle(0)

def left_rotate(clockwise = True,pwm = None):
	pins = Cfg().get('left_motor')
	en = pin(pins['EN'])
	in1 = pin(pins['IN1'])
	in2 = pin(pins['IN2'])

	return rotate(clockwise,en,in1,in2,pwm)

def right_rotate(clockwise = True,pwm = None):
        pins = Cfg().get('right_motor')
        en = pin(pins['EN'])
        in1 = pin(pins['IN1'])
        in2 = pin(pins['IN2'])

        return rotate(clockwise,en,in1,in2,pwm)

def left_stop(pwm):
        pins = Cfg().get('left_motor')
        en = pin(pins['EN'])
        in1 = pin(pins['IN1'])
        in2 = pin(pins['IN2'])

	stop(en,in1,in2,pwm)

def right_stop(pwm):
        pins = Cfg().get('right_motor')
	en = pin(pins['EN'])
        in1 = pin(pins['IN1'])
        in2 = pin(pins['IN2'])

	stop(en,in1,in2,pwm)

led = Cfg().get('ctrl_led')
GPIO.setup(led,GPIO.OUT)

while True:
	#turn led on
	GPIO.output(led,GPIO.HIGH)

	#test left motor 
	left_pwm = left_rotate(True,left_pwm)
	sleep(1)
	left_stop(left_pwm)

        GPIO.output(led,GPIO.LOW)

	left_rotate(False,left_pwm)
	sleep(1)
	left_stop(left_pwm)

        GPIO.output(led,GPIO.HIGH)

	#test right motor
	right_pwm = right_rotate(True,right_pwm)
	sleep(1)
	right_stop(right_pwm)

        GPIO.output(led,GPIO.LOW)

	right_rotate(False,right_pwm)
	sleep(1)
	right_stop(right_pwm)

        GPIO.output(led,GPIO.HIGH)

	#test both motors
	left_rotate(False,left_pwm)
	right_rotate(False,right_pwm)
	sleep(2)
	left_stop(left_pwm)
	right_stop(right_pwm)

        GPIO.output(led,GPIO.LOW)

	left_rotate(True,left_pwm)
	right_rotate(True,right_pwm)
	sleep(2)
	left_stop(left_pwm)
	right_stop(right_pwm)

        GPIO.output(led,GPIO.LOW)

	sleep(5)

left_pwm.stop()
right_pwm.stop()

GPIO.output(led,GPIO.LOW)

GPIO.cleanup()
