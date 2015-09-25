## Python script using RasPi to store the shower time and date using simple I/O push button interface
##

import datetime
import sys
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

out1=13
out2=26
out3=27
in1=12

GPIO.setup(out1,GPIO.OUT)
GPIO.setup(out2,GPIO.OUT)
GPIO.setup(out3,GPIO.OUT)
GPIO.setup(in1,GPIO.IN)

GPIO.output(out1,False)
GPIO.output(out2,False)
GPIO.output(out3,False)

def current_time(): # returns current hour, min and second in military time
	rn= datetime.datetime.now()
	#now= datetime.time(rn.hour, rn.minute,rn.second)
	return rn

def main():
	now=current_time()
	# When the button is pressed
	while GPIO.input(in1): # PRESSING BUTTON IS NOT A STEP FN
		# Turn on Red LED
		GPIO.output(out1, TRUE)
		#Wait for another press


# Getting the current time...
timenow= time.time()
bool inShower


while inShower