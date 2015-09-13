
import datetim

import sys
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)	
GPIO.setmode(GPIO.BCM)

led=13
bttn=12

GPIO.setup(led, GPIO.OUT)


while 1:
	GPIO.output(led,True)
	print('1')
	time.sleep(0.2)
	print('2')
	GPIO.output(led,False)
	time.sleep(0.2)





def current_time(): # returns current hour, min, and second in military time
    RN = datetime.datetime.now()
    now = datetime.time(RN.hour, RN.minute, RN.second)
    return now


def set_timeline(): # makes the timeline 

    ############ User 1
    user1 = 'Deven'
    user1_start_time = datetime.time(02,00,0)
    user1_end_time = datetime.time(02,31,0)

    ############ User 2
    user2 = 'Albert'
    user2_start_time = datetime.time(02,31,0)
    user2_end_time = datetime.time(02, 44,0)

    ############ User 3
    user3 = 'Spencer'
    user3_start_time = datetime.time(02,46,0)
    user3_end_time = datetime.time(02,51,0)

    ############ User 4
    user4 = 'Noah'
    user4_start_time = datetime.time(02,51,0)
    user4_end_time = datetime.time(02,59,0)

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
    print "UC"
    return

def state_SO(scheduled_user): # scheduled and open, 
    print "SO"
    print scheduled_user, "is scheduled to use shower, but has not begun yet"
    return    

def state_SC(scheduled_user, scheduled_user_end_time):
    print "SC"
    print type(scheduled_user_end_time)
    print (datetime.time(minutes=1))
   # warning_time = scheduled_user_end_time + datetime.strptime('1', %M)
    while (current_time() < warning_time): # nothing wrong, user in shower
        while shower_state == True:
            print scheduled_user, "is scheduled and currently using...waiting..."
            if (current_time() == warning_time) & (shower_state == True):
                print "one min left"
                while ((current_time() > warning_time) & (shower_state == True)):
                    print scheduled_user, "is going over time"

        if shower_state == False:
            return

def main():
    shower_state = True
    timeline = set_timeline()
    print_timeline(timeline)
    if determine_current_turn(timeline) == False: # unscheduled
        if shower_state == False: # open U.O.
            state_UO()
        elif shower_state == True: # closed U.C.
            state_UC()
    else:  # scheduled
        scheduled_user = determine_current_turn(timeline)[0]
        scheduled_user_end_time = determine_current_turn(timeline)[2]
        print "Current shower time belongs to" , scheduled_user, "because the time is", current_time()
        if shower_state == False: # open S.O.
            state_SO(scheduled_user)

        elif shower_state == True: # closed S.C.
            state_SC(scheduled_user, scheduled_user_end_time)
            



if __name__ == "__main__":
    main()
