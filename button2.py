import RPi.GPIO as GPIO           # import RPi.GPIO module  
GPIO.setmode(GPIO.BCM)            # choose BCM or BOARD  
GPIO.setup(port_or_pin, GPIO.OUT) # set a port/pin as an output   
GPIO.output(port_or_pin, 1)       # set port/pin value to 1/GPIO.HIGH/True  
GPIO.output(port_or_pin, 0)       # set port/pin value to 0/GPIO.LOW/False  
