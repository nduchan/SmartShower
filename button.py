import RPi.GPIO as GPIO
import time
import os

led=24
bttn=18

GPIO.setmode(GPIO.BMC)
GPIO.setup(bttn, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # initial button is off
GPIO.setup(led, GPIO.OUT, pull_up_down=GPIO.PUD_DOWN)  # initial led is off

def button_state():
	while True:
		shower_state = GPIO.input(bttn)
		time.sleep(0.5)
		return shower_state
		GPIO.output(led,shower_state)
		GPIO.add_event_detect(bttn, GPIO.RISING, callback=my_callback_closed, bouncetime=500)
		GPIO.add_event_detect(bttn, GPIO.FALLING, callback=my_callback_open, bouncetime=500)


def my_callback_closed():	
	print('Somebody entered the shower')

def my_callback_open():
	print('Somebody exited the shower')
