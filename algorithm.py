
import datetime


class UserObj:
	"""A class containing user info"""


	def __init__(self, name_in, length_in, time_in, event_in=None):
		self.userName = name_in
		self.showerLengthPref = length_in
		self.timeBeforeEventPref = time_in
		self.firstEvent = event_in



def handle_collision(begin, end, person, array_in):
	earliest = begin
	for i, x in enumerate(array_in):
		if x[0] < begin:
			earliest = x[0]

		#condition where collision is first and second event
		#push first event earlier by difference
		#----------B------E-----------added
		#-----B------E----------------new
		#becomes
		#----------B------E-----------added
		#--B------E-------------------new
		if end > x[0] and earliest == begin:
			print 'jack and jill'
			begin = begin - (end-x[0])
			end = end - (end - x[0])
			array_in.append([begin, end, person])
			return array_in

		elif begin == x[0] and end == x[1]:
			print array_in[i][0], array_in[i][1], array_in[i][2]
			array_in[i][1] = begin =begin+ (end-begin)/2
			array_in.append([begin, end, person])
			return array_in

		#condition where collision is last event
		#split difference between colliding events
		#----------B-----------E----------added
		#-----------------B---------E-----new
		#becomes
		#----------B--------E-------------added
		#--------------------B------E-----new
		elif i == len(array_in)-1:
			print ' clairie'
			begin = begin + (end-x[1])/2
			array_in[i][1] = array_in[i][1] - (end-x[1])/2
			array_in.append([begin, end, person])
			return array_in

		elif begin < x[1] and end <= array_in[i+1][0]:
			print 'sydney'
			begin = begin + (end-x[1])/2
			array_in[i][1] = array_in[i][1] - (end-x[1])/2
			array_in.append([begin, end, person])
			return array_in

		elif begin < x[1] and end >= array_in[i+1][0]:
			print 'collide!!!!!!!!!!'
			print x[2]
			print x[0], x[1]
			print begin, end, person
			end = end - (end - array_in[i+1][0])/2
			array_in[i+1][0] = array_in[i+1][0] - (end - array_in[i+1][0])/2
			array_in.append([begin, end, person])
			return array_in



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
			outArray = handle_collision(ptimeBegin, ptimeEnd, user[0], outArray)
		else:
			outArray.append([ptimeBegin, ptimeEnd, user[0]])
		outArray = sortIt(outArray)

	return outArray

def main():

	Users = []

	""" 0 - username, 1 - event stat, 2 - shower time, 3 - prefered time before event"""
	Deven = ('Deven', datetime.datetime.strptime('8:00:00', '%H:%M:%S'), 10, datetime.datetime.strptime('1:00:00', '%H:%M:%S'))
	Albert = ('Albert', datetime.datetime.strptime('8:00:00', '%H:%M:%S'), 10, datetime.datetime.strptime('1:00:00', '%H:%M:%S'))
	Noah = ('Noah', datetime.datetime.strptime('8:00:00', '%H:%M:%S'), 10, datetime.datetime.strptime('1:00:00', '%H:%M:%S'))
	Users.append(Deven)
	Users.append(Albert)
	Users.append(Noah)
	outSchedule = calc_best(Users)
	print 'SCHEDULE'
	print '----------------------'
	print outSchedule
	print outSchedule[0][0], outSchedule[0][1], outSchedule[0][2]
	print outSchedule[1][0], outSchedule[1][1], outSchedule[1][2]
 	print outSchedule[2][0], outSchedule[2][1], outSchedule[2][2]

if __name__ == "__main__": main()

