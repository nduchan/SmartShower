
import datetime


class UserObj:
	"""A class containing user info"""


	def __init__(self, name_in, length_in, time_in, event_in=None):
		self.userName = name_in
		self.showerLengthPref = length_in
		self.timeBeforeEventPref = time_in
		self.firstEvent = event_in


def get_long(new_start, new_end, scheduled_start, scheduled_end):
	if scheduled_end - new_start > new_end - scheduled_start:
		return 0
	else:
		return 1

def single_double(new_start, new_end, first_start, first_end):
	collision = 0
	if new_start >= first_start and new_start < first_end:
		collision += 1
	elif new_end <= first_end and new_end > first_start:
		collision += 1
	return collision

def handle_collision(begin, end, person, array_in):
	earliest = begin
	for i, x in enumerate(array_in):
		maximize = 0  #0 -> take new start old end, #1 -> take old start new finish
		single_collision = single_double(begin, end, x[0], x[1])
		if single_collision == 0:
			continue
		else:
			maximize = get_long(begin, end, x[0], x[1])
			if maximize:
				begin = array_in[i][1] = x[1]- (x[1]-begin)/2
			else:
				end = array_in[i][0] = end- (end-x[0])/2

		return [begin, end, person]

def getKey(item, self):
	return item[0]


def sortIt(array_in):
	array_in = sorted(array_in, key=lambda time:time[0])
	return array_in



def check_collision(begin, end, array_in):
	if not array_in:
		return True
	for x in array_in:
		if begin < x[1] and begin > x[0]:
			return False
		if end > x[0] and begin < x[1]:
			return False
	return True


def calc_best(userList_in):
	outArray = []
	for user in userList_in:
		ptimeEnd = user[1]-user[3]
		ptimeBegin = ptimeEnd-datetime.timedelta(minutes=user[2])
		check_out = check_collision(ptimeBegin, ptimeEnd, outArray)
		if not check_out:
			holder = handle_collision(ptimeBegin, ptimeEnd, user[0], outArray)
			holder = handle_collision(holder[0], holder[1], holder[2], outArray)
			outArray.append(holder)
		else:
			outArray.append([ptimeBegin, ptimeEnd, user[0]])
		outArray = sortIt(outArray)

	return outArray

def main():

	Users = []

	""" 0 - username, 1 - event stat, 2 - shower time, 3 - prefered time before event"""
	Deven = ('Deven', datetime.datetime.strptime('4:00:00', '%H:%M:%S'), 30, datetime.datetime.strptime('1:00:00', '%H:%M:%S'))
	Albert = ('Albert', datetime.datetime.strptime('3:30:00', '%H:%M:%S'), 30, datetime.datetime.strptime('1:00:00', '%H:%M:%S'))
	Noah = ('Noah', datetime.datetime.strptime('3:45:00', '%H:%M:%S'), 30, datetime.datetime.strptime('1:00:00', '%H:%M:%S'))
	#Spencer = ('Spencer', datetime.datetime.strptime('8:00:00', '%H:%M:%S'), 10, datetime.datetime.strptime('1:00:00', '%H:%M:%S'))
	Users.append(Deven)
	Users.append(Albert)
	Users.append(Noah)
	#Users.append(Spencer)
	outSchedule = calc_best(Users)
	print 'SCHEDULE'
	print '----------------------'
	print outSchedule
	print outSchedule[0][0], outSchedule[0][1], outSchedule[0][2]
	print outSchedule[1][0], outSchedule[1][1], outSchedule[1][2]
 	print outSchedule[2][0], outSchedule[2][1], outSchedule[2][2]
  	#print outSchedule[3][0], outSchedule[3][1], outSchedule[3][2]

if __name__ == "__main__": main()

