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



def current_time(): # returns current hour, min, and second in military time
	RN = datetime.datetime.now()
	#now = datetime.time(RN.hour, RN.minute, RN.second)
	return RN


def set_timeline(): # makes the timeline 

	############ User 1
	user1 = 'Deven'
	user1_start_time = datetime.datetime(2015,9,13,11,40,0)
	user1_end_time = datetime.datetime(2015,9,13,11,45,0)

	############ User 2
	user2 = 'Albert'
	user2_start_time = datetime.datetime(2015,9,13,13,32,0)
	user2_end_time = datetime.datetime(2015,9,13,14,00,0)

	############ User 3
	user3 = 'Spencer'
	user3_start_time = datetime.datetime(2015,9,13,15,01,0)
	user3_end_time = datetime.datetime(2015,9,13,16,30,0)

	############ User 4
	user4 = 'Noah'
	user4_start_time = datetime.datetime(2015,9,17,11,30,0)
	user4_end_time = datetime.datetime(2015,9,18,12,00,0)

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
	state= 'UO'
	print state
	turn_off_all_led()
	return

def state_UC(): #U & Closed, no problems, normal operations
	GPIO.output(red_led,True) # red light indicates closed
	state= 'UC'
	print state
	return

def state_SO(state,scheduled_user, scheduled_user_start_time, scheduled_user_end_time): # scheduled and open, 
	turn_off_all_led()
	shower_state=state
	GPIO.output(green_led,True) # green light indicates scheduled
	print shower_state
	print scheduled_user, "is scheduled to use shower, but has not begun yet"
	while 1:
		if (GPIO.input(button) == True) & (shower_state =='SO'):
			time.sleep(1)
			return False
		elif current_time() >= scheduled_user_start_time:
			flash_all()
			return

	return    

def state_SC(shower_state,scheduled_user, scheduled_user_end_time):
	turn_off_all_led()
	shower_state=state
	warning_time= scheduled_user_end_time - datetime.timedelta(0,60)
	while 1:
		if GPIO.input(button):
			time.sleep(1)
			return False
		elif (current_time() <= warning_time): #User is on time and in the shower
			print scheduled_user, 'is currently scheduled and in the shower...'
			GPIO.output(red_led,True) # red light indicates closed
			GPIO.output(green_led,True) # green light indicates scheduled
		elif (current_time() >= warning_time) &  (current_time() <= scheduled_user_end_time): # User has <1 minute
			GPIO.output(yellow_led, TRUE) # <1 minute left
			## ADD SIREN SOUNDZZZZ 
			print scheduled_user, 'has less than a minute for their scheduled shower time'
		elif (current_time() > scheduled_user_end_time):
			turn_off_all_led()
			flash_all()

			#amt= current_time() - scheduled_user_end_time # Calculate amount owed
			#if amt == integer
				# BUZ
			#amt= 
			#print scheduled_user, 'is over their allotted shower duration. Owes ', amt ,' dollars'
		else:
			print 'either UC or UO'

	return

#############

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
	timeline = set_timeline()
	print_timeline(timeline)
	#state = 'SO'
	# Determine State and Loop
	while 1:
		if determine_current_turn(timeline) == False: # Unscheduled
			state_UO()
		if current_time() >=  (timeline[3][2] + datetime.timedelta(minutes=15)): # Time is after the end of the last person's shower, thus Unscheduled & Closed
			state_UC()
		else:  # scheduled
			scheduled_user = determine_current_turn(timeline)[0]
			scheduled_user_end_time = determine_current_turn(timeline)[2]
			   # print "Current shower time belongs to" , scheduled_user, "because the time is", current_time()
			if state == 'SO':
				if state_SO(state, scheduled_user, scheduled_user_start_time, scheduled_user_end_time)==False:
					state='SC'
			if state == 'SC':
				if state_SC(state, scheduled_user, scheduled_user_end_time)==False:
					state='SO'




if __name__ == "__main__":
	main()
	exit()





