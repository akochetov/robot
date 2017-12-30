from gpiozero import Button
from subprocess import check_call
from subprocess import Popen
from signal import pause
from time import time

#---------------------------------------
#constants
dbl_press_time = 0.25 #in seconds
p=None
#---------------------------------------
#global variables
press_time = 0

#---------------------------------------
#button press handlers

def when_held():
	print('Button held. Shutting down...')
	check_call('sudo poweroff ',shell=True)

def when_pressed():
	#inform python that we will use global press_time variable
	global press_time
	global p

	if (time()-press_time)<=dbl_press_time:
		print('Dbl click detected')
		if p is not None:
			p.kill()
			p=None
	else:
		print('Button pressed')
		if p is None:
			p=Popen('exec python /home/pi/led.py',shell=True)
	press_time = time()

#----------------------------------------
#create GPIO button. This will init GPIO (takes a few secs)
shut_btn=Button(26,hold_time=3)

#----------------------------------------

print('GPIO is ready.')
shut_btn.when_held=when_held
shut_btn.when_pressed=when_pressed
pause()
