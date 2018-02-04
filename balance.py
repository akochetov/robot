import math
from config import Cfg
from time import sleep, time
from gyro import MPU6050
#from mpu6050 import MPU6050
from motor import PWMMotor

def sign(x): return 1 if x >= 0 else -1

sleep_time = 1/Cfg().get("frequency")

delta   = 0 #difference between current angle and target angle
error   = 0 #integral (sum) of deltas for last balancing cycles
preva	= 0

prev_time	= 0 #time of previous balance cycle, used to calculate gyro angle offsets basing on gyro angle speeds

print "Creating MPU instance on address:",str(hex(Cfg().get("gyro")["address"]))
mpu = MPU6050(Cfg().get("gyro")["address"])
axis = Cfg().get("gyro")["axis"]
max_angle = Cfg().get("max_angle")
target = Cfg().get("gyro")["target"]
calibration = Cfg().get("gyro")["calibration"]

K1 = Cfg().get("gyro_filter")["K1"]
K2 = Cfg().get("gyro_filter")["K2"]

lmotor = PWMMotor(Cfg().get("lmotor")["EN"],Cfg().get("lmotor")["IN1"],Cfg().get("lmotor")["IN2"])
rmotor = PWMMotor(Cfg().get("rmotor")["EN"],Cfg().get("rmotor")["IN1"],Cfg().get("rmotor")["IN2"])

lmotor.setup()
rmotor.setup()

#function requests gyro/accel 10 times and takes an average angle from accelerometer to consider it as a base angle for further gyro offsets
def initAngle():
	mpu.updateData()
	s = 0
	for i in range(0,10):
                if axis=="x":
                        s += mpu.getXrotation()
                elif axis=="y":
                        s += mpu.getYrotation()
                else:
                        raise AttributeError("Unknown axis specified: "+axis)
	return s/10

#get initial angle from accelerometer
angle = initAngle()
prev_time = time()
print "initial angle:",angle

while True:
	mpu.updateData()

        time_diff = time()-prev_time
        prev_time = time()
	offset = 0
        if axis=="x":
                offset = time_diff * (mpu.getXoutSc()+calibration)
		angle = K1 * (angle + offset) + K2 * (mpu.getXrotation())
        elif axis=="y":
                offset = time_diff * (mpu.getYoutSc()+calibration)
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
  
    	delta = angle - target
    	min_power = 100
    	power=min_power+math.fabs(delta/max_angle*(100-min_power))#-math.fabs(sume*ki)-(balance-delta/45*100*kd)

    	clockwise = delta > 0
    	lmotor.rotate(clockwise,power)
    	rmotor.rotate(clockwise,power)

	sleep(sleep_time)#sleep until next balancing cycle
