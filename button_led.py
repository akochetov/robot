from gpiozero import LED,Button
from signal import pause

led=LED(15)
button=Button(14)

def button_pressed():
	print('button pressed')
	led.on()

def button_released():
	print('button released')
	led.off()

print('ready')

button.when_pressed=button_pressed
button.when_released=button_released

pause()

