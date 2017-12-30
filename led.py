import time
from gpiozero import LED

led = LED(21)

for i in range(0,10):
	led.on()
	print('led on\r\n')
	time.sleep(1)
	led.off()
	print('led off\r\n')
	time.sleep(1)
