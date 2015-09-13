# Converts Time



import datetime

def main():

	user_time= datetime.datetime.now()

	warning_time = user_time - datetime.timedelta(minutes=30) #datetime.datetime.strptime('00:01:00', '%H:%M:%S')
    #warning_time = datetime.datetime.combine(datetime.date.today(), scheduled_user_end_time) - datetime.timedelta(minutes=1)
    #datetime.datetime.strptime('00:01:00', '%H:%M:%S')

	#warning_time= datetime.timedelta(0,0,0,0,1)

	print current_time() >=  (timeline[3][2] + datetime.timedelta(minutes)):

	#print warning_time

	#new_time= datetime.datetime(2015,9,13,11,00,0) - datetime.datetime.now()
	#new_time= new_time.strftime('%H:%M:%S')
	#new_time= datetime.datetime.strptime(new_time, '%M')
	#print new_time


def current_time(): # returns current hour, min, and second in military time
	RN = datetime.datetime.now()
	#now = datetime.time(RN.hour, RN.minute, RN.second)
	return RN


if __name__ == "__main__":
	main()
