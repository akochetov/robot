import RPi.GPIO as IO          # calling header file which helps us use GPIOs of PI
import time                    # calling time to provide delays in program
import sys

pin = int(sys.argv[1])
duty = int(sys.argv[2])

print("You specified: pin - "+str(pin)+", duty cycle in % - "+str(duty))

print("Initializing GPIO...")
IO.setmode(IO.BCM)           #we are programming the GPIO by BCM pin numbers
IO.setup(pin,IO.OUT)         # initialize as an output.

print("Setting PWM on pin "+str(pin))
p = IO.PWM(pin,100)        #GPIO pin as PWM output, with 100Hz frequency

print("Start PWM with duty - "+str(duty))
p.start(duty)                            #generate PWM signal with given duty cycle

#p.ChangeDutyCycle(x)                 #change duty cycle for changing the brightness of LED.

print("Press Enter to stop")
input()
p.stop()

IO.cleanup()
