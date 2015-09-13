import RPi.GPIO as GPIO           # import RPi.GPIO module  
GPIO.setmode(GPIO.BCM)            # choose BCM or BOARD  
led = 16
btn = 12
GPIO.setup(led, GPIO.OUT)    

try:  
    while True:  
        GPIO.output(led, 1)         # set GPIO16 to 1/GPIO.HIGH/True  
        sleep(0.2)                
        GPIO.output(led, 0)         # set GPIO16 to 0/GPIO.LOW/False  
        sleep(0.2)                
  
except KeyboardInterrupt:          # trap a CTRL+C keyboard interrupt  
    GPIO.cleanup()                 # resets all GPIO ports used by this program 
