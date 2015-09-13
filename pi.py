import datetime
import sys
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)	
GPIO.setmode(GPIO.BCM)

red_led=13
green_led = 26 
button=12
yellow_led = 27

GPIO.setup(yellow_led, GPIO.OUT)
GPIO.setup(red_led, GPIO.OUT)
GPIO.setup(green_led, GPIO.OUT)

GPIO.setup(button, GPIO.IN)

GPIO.output(red_led,False)
GPIO.output(green_led,False)
GPIO.output(yellow_led,False)


def switch(button):
	if (GPIO.input(button) & (occupied ==0)):
		occupied = 1
		print occupied
		return occupied
	else:
		return occupied


def current_time(): # returns current hour, min, and second in military time
    RN = datetime.datetime.now()
    now = datetime.time(RN.hour, RN.minute, RN.second)
    return now


def set_timeline(): # makes the timeline 

    ############ User 1
    user1 = 'Deven'
    user1_start_time = datetime.time(04,00,0)
    user1_end_time = datetime.time(04,31,0)

    ############ User 2
    user2 = 'Albert'
    user2_start_time = datetime.time(04,31,0)
    user2_end_time = datetime.time(04, 46,0)

    ############ User 3
    user3 = 'Spencer'
    user3_start_time = datetime.time(04,46,0)
    user3_end_time = datetime.time(04,51,0)

    ############ User 4
    user4 = 'Noah'
    user4_start_time = datetime.time(04,51,0)
    user4_end_time = datetime.time(04,59,0)

    timeline = [[user1, user1_start_time, user1_end_time],
            [user2, user2_start_time, user2_end_time],
            [user3, user3_start_time, user3_end_time],
            [user4, user4_start_time, user4_end_time]]
    return timeline

def print_timeline(timeline):
    for i in timeline:
        print "name:", i[0]
        print "start time:" , i[1]
        print "end time: " , i[2]
        print 

def determine_current_turn(timeline):
    for i in timeline:
        if (i[1] < current_time() < i[2]):
            return i 
    return False




def state_UO(): # U & open, no problems, normal operations
    print "UO"
    return

def state_UC(): #U & Closed, no problems, normal operations
    GPIO.output(red_led,True) # red light indicates closed
    print "UC"
    return

def state_SO(scheduled_user, scheduled_user_end_time): # scheduled and open, 
    turn_off_all_led()
    GPIO.output(green_led,True) # green light indicates scheduled
    print "SO"
    print scheduled_user, "is scheduled to use shower, but has not begun yet"
    while 1:
		if GPIO.input(button) == True:
			occupied = True
			if state_SC(scheduled_user, scheduled_user_end_time) == 0: return


    return    

def state_SC(scheduled_user, scheduled_user_end_time):
    GPIO.output(red_led,True) # red light indicates closed
    GPIO.output(green_led,True) # green light indicates scheduled
    print "SC"

   # warning_time = scheduled_user_end_time - datetime.timedelta(0,0,0,0,1) #datetime.datetime.strptime('00:01:00', '%H:%M:%S')
    warning_time = datetime.time(04,56,0)

    occupied = True
    while (current_time() <= warning_time): # nothing wrong, user in shower
        while occupied == True:
            print scheduled_user, "is scheduled and currently using...waiting..."
            while 1:
				if GPIO.input(button):
					occupied = 0
					return occupied
				if (current_time() == warning_time) & (occupied == True):
					GPIO.output(yellow_led,True) # yellow light indicates warning
		            print "one min left"
		            while ((current_time() >= warning_time) & (occupied == True)):
		                print scheduled_user, "is going over time"
		                while 1:
						flash_all()
						print 'fadsfasdfa', GPIO.input(button)
						if(GPIO.input(button)):
							GPIO.output(red_led,0)
							GPIO.output(green_led,0)
							GPIO.output(yellow_led,0)
							occupied = 0
							turn_off_all_led()
							return occupied
    if occupied == False:
        return

def flash_all():
	
	GPIO.output(red_led,1)
	time.sleep(.1)
	GPIO.output(red_led,0)
	GPIO.output(yellow_led,1)
	time.sleep(.1)
	GPIO.output(yellow_led,0)
	GPIO.output(green_led,1)
	time.sleep(.1)
	GPIO.output(green_led,0)

def turn_off_all_led():
	GPIO.output(green_led,0)
	GPIO.output(red_led,0)
	GPIO.output(yellow_led,0)

def main():
    occupied = False
    timeline = set_timeline()
    print_timeline(timeline)
    while 1:
		if determine_current_turn(timeline) == False: # unscheduled
		    if occupied == False: # open U.O.
		        state_UO()
		    elif occupied == True: # closed U.C.
		        state_UC()
		else:  # scheduled
		    scheduled_user = determine_current_turn(timeline)[0]
		    scheduled_user_end_time = determine_current_turn(timeline)[2]
		    print "Current shower time belongs to" , scheduled_user, "because the time is", current_time()
		    if occupied == False: # open S.O.
		        state_SO(scheduled_user, scheduled_user_end_time)

		    elif occupied == True: # closed S.C.
		        if state_SC(scheduled_user, scheduled_user_end_time) == False:
					GPIO.output(green_led,1)
		        



if __name__ == "__main__":
	main()
	exit()





