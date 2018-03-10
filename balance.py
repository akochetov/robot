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
prev_angle	= 0 #angle captured during previous balancing cycle
sleep_time = 1.0/Cfg().get("frequency")


#reading configuration parameters once at the beginning
print "Creating MPU instance on address:",str(hex(Cfg().get("gyro")["address"]))
mpu = MPU6050(Cfg().get("gyro")["address"])	#address of mpu6050 in I2C bus space
axis = Cfg().get("gyro")["axis"]		#axis to balance (x or y)
max_angle = Cfg().get("max_angle")		#max angle. when current angle gets above max - stop motors
target = Cfg().get("gyro")["target"]		#angle to keep
calibration = Cfg().get("gyro")["calibration"]	#gyro calibration (offset) for selected axis 
min_power = Cfg().get("min_power")		#minimum power to supply to motors. from 0 to 100.
max_power = Cfg().get("max_power")
led = Cfg().get("ctrl_led")
lmotor_balance = Cfg().get("motors_balance")["left"]
rmotor_balance = Cfg().get("motors_balance")["right"]

K1 = Cfg().get("gyro_filter")["K1"]		#complimentary filter coeficient. gyro coeficient
K2 = Cfg().get("gyro_filter")["K2"]		#complimentary filter coeficient. accelerometer coefficent

P = Cfg().get("pid")[0]
I = Cfg().get("pid")[1]
D = Cfg().get("pid")[2]

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
prev_angle = angle
prev_time = time()
print "initial angle:",angle

#setup led to indicate program status
GPIO.setmode(GPIO.BCM)
GPIO.setup(led,GPIO.OUT)
GPIO.output(led,GPIO.HIGH)

while not exit_loop:
	#fetch data from gyro and accel
        time_diff = time()-prev_time
        prev_time = time()
	mpu.updateData()
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
 	if math.fabs(angle-target) > max_angle:
        	print "Angle exceeds maximum angle"
        	lmotor.stop()
        	rmotor.stop()
        	continue

	#calulcate power to supplty to motors  
    	delta = angle - target
	delta_sign = 1 if delta > 0 else -1
	future_angle = 2*angle-prev_angle

    	power = min_power+P*math.fabs(delta/max_angle*(100-min_power))-\
		I*math.fabs(delta)-\
		D*delta_sign*(target-future_angle)

	if power > max_power:
		power = max_power
	if power < 0:
		power = min_power

	print "d = {}	power = {}	P = {}	I = {}	t = {}	a = {}	prev_a = {}	future_a = {}	D = {}".format(delta,power,P*math.fabs(delta/max_angle*(100-min_power)),I*math.fabs(delta),target,angle,prev_angle,future_angle,D*delta_sign*(target-future_angle))


	#identify rotation direction
    	clockwise = delta > 0
    	lmotor.rotate(clockwise,power*lmotor_balance)
    	rmotor.rotate(clockwise,power*rmotor_balance)

	sleep(sleep_time)#sleep until next balancing cycle

	#remember angle for piD calculations during next balancing cycle
	prev_angle = angle

print "Received terminalion signal. Exiting."
lmotor.stop()
rmotor.stop()
GPIO.output(led,GPIO.LOW)

