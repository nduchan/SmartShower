import RPi.GPIO as GPIO
import time
import os

led=22
bttn=18

GPIO.setup(bttn, GPIO.IN, initial=False) # initial button is off
GPIO.setup(led, GPIO.OUT, initial=False)  # initial led is off
GPIO.setmode(GPIO.BOARD)

def button_state():
	while True:
		shower_state = GPIO.input(bttn)
		time.sleep(0.5)
		return shower_state
		GPIO.output(led,shower_state)


def my_callback_closed():	
	print('Somebody entered the shower')
	GPIO.add_event_detect(bttn, GPIO.RISING, callback=my_callback_closed, bouncetime=500)

def my_callback_open():
	print('Somebody exited the shower')
	GPIO.add_event_detect(bttn, GPIO.FALLING, callback=my_callback_open, bouncetime=500)
