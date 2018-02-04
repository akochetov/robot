import math
import RPi.GPIO as GPIO
from signal import signal,SIGINT,SIGTERM
from config import Cfg
from time import sleep, time
from gyro import MPU6050
from motor import PWMMotor

delta   = 0 #difference between current angle and target angle
error   = 0 #integral (sum) of deltas for last balancing cycles
prev_time	= 0 #time of previous balance cycle, used to calculate gyro angle offsets basing on gyro angle speeds
sleep_time = 1/Cfg().get("frequency")


#reading configuration parameters once at the beginning
print "Creating MPU instance on address:",str(hex(Cfg().get("gyro")["address"]))
mpu = MPU6050(Cfg().get("gyro")["address"])	#address of mpu6050 in I2C bus space
axis = Cfg().get("gyro")["axis"]		#axis to balance (x or y)
max_angle = Cfg().get("max_angle")		#max angle. when current angle gets above max - stop motors
target = Cfg().get("gyro")["target"]		#angle to keep
calibration = Cfg().get("gyro")["calibration"]	#gyro calibration (offset) for selected axis 
min_power = Cfg().get("min_power")		#minimum power to supply to motors. from 0 to 100.
led = Cfg().get("ctrl_led")

K1 = Cfg().get("gyro_filter")["K1"]		#complimentary filter coeficient. gyro coeficient
K2 = Cfg().get("gyro_filter")["K2"]		#complimentary filter coeficient. accelerometer coefficent

#initializing motors
lmotor = PWMMotor(*Cfg().get("lmotor").values())
rmotor = PWMMotor(*Cfg().get("rmotor").values())
lmotor.setup()
rmotor.setup()

#function requests gyro/accel 10 times and takes an average angle from accelerometer to consider it as a base angle for further gyro offsets
def initAngle():
	s = 0
	#fetch data from accelerometer 10 times and calulcate the angle
	for i in range(0,10):
		mpu.updateData()
                if axis=="x":
                        s += mpu.getXrotation()
                elif axis=="y":
                        s += mpu.getYrotation()
                else:
                        raise AttributeError("Unknown axis specified: "+axis)
	#now return average accelrometer-based angle to reduce noise for initial gyro angle
	return s/10

exit_loop = False
def exitLoop(arg1,arg2):
	global exit_loop
	exit_loop = True
signal(SIGINT, exitLoop)
signal(SIGTERM, exitLoop)

#get initial angle from accelerometer
angle = initAngle()
prev_time = time()
print "initial angle:",angle

#setup led to indicate program status
GPIO.setmode(GPIO.BCM)
GPIO.setup(led,GPIO.OUT)
GPIO.output(led,GPIO.HIGH)

while not exit_loop:
	#fetch data from gyro and accel
	mpu.updateData()

        time_diff = time()-prev_time
        prev_time = time()
	offset = 0

	#recalulate gyro angle taking gyro data into account
        if axis=="x":
                offset = time_diff * (mpu.getXoutSc()+calibration)
		#apply complimentary filter
		angle = K1 * (angle + offset) + K2 * (mpu.getXrotation())
        elif axis=="y":
                offset = time_diff * (mpu.getYoutSc()+calibration)
		#apply complimentary filter
		angle = K1 * (angle + offset) + K2 * (mpu.getYrotation())
        else:
                raise AttributeError("Unknown axis specified: "+axis)

    	#print "gyro angle:",str(angle)
	#print "accel angle:",str(mpu.getXrotation())
 	if math.fabs(angle) > max_angle:# or math.fabs(angle) < 1:
        	print "Angle exceeds maximum angle."
        	lmotor.stop()
        	rmotor.stop()
        	continue

	#calulcate power to supplty to motors  
    	delta = angle - target
    	power=min_power+math.fabs(delta/max_angle*(100-min_power))#-math.fabs(sume*ki)-(balance-delta/45*100*kd)

	#identify rotation direction
    	clockwise = delta > 0
    	lmotor.rotate(clockwise,power)
    	rmotor.rotate(clockwise,power)

	sleep(sleep_time)#sleep until next balancing cycle

print "Received terminalion signal. Exiting."
GPIO.output(led,GPIO.LOW)

