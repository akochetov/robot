from gpiozero import MotionSensor,LED
from signal import pause
 
motionball=MotionSensor(26)
ledred=LED(21)
motionball.when_motion=ledred.on
motionball.when_no_motion=ledred.off
pause()
