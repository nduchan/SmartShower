import flask
from flask import Flask
from flask.ext.mysqldb import MySQL
from flask import render_template
from flask import request
from flask import json
from werkzeug import generate_password_hash, check_password_hash
from oauth2client import client
import httplib2
import json
from apiclient import discovery
import datetime

CLIENT_ID = "456555048105-49j7n97kvjuluk4f0b3598m70sk0e293"
SCOPE = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'SmartShower'

app = Flask(__name__)
mysql = MySQL()

app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'SmartShowerDB'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'

mysql.init_app(app)

##################################################################

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

def get_user_events(address_in):
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute("SELECT fname, event, duration, buffer FROM smartshowerdb.users WHERE event IS NOT NULL AND address='{0}'".format(address_in))
    result = cursor.fetchall()
    new_result = []
    for user in result:
        new_user = []
        for item in user:
            new_user.append(item)
        new_result.append(new_user)
    return new_result

def convert_times(Users_in):
    for i, user in enumerate(Users_in):
        Users_in[i][3] = datetime.datetime.strptime('00:'+str(user[3])+':00', '%H:%M:%S')
    return Users_in

def write_calendar(list_in):
    if datetime.datetime.now() < datetime.datetime.strptime('06:00:00', '%H:%M:%S'):
        scanner = datetime.datetime.combine(datetime.datetime.today(), datetime.datetime.strptime('00:00:00', '%H:%M:%S').time())
    else:
        scanner = datetime.datetime.combine(datetime.datetime.today()+ datetime.timedelta(days=1), datetime.datetime.strptime('00:00:00', '%H:%M:%S').time())

    scanner_end = scanner+datetime.timedelta(days=1)
    scanner = scanner.isoformat()+'Z'
    scanner_end = scanner_end.isoformat()+ 'Z'
    credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
    http_auth = credentials.authorize(httplib2.Http())
    cal_service = discovery.build('calendar', 'v3', http_auth)

    eventsResult = cal_service.events().list(
        calendarId=flask.session['calendar_id'], timeMin=scanner, timeMax=scanner_end, maxResults=25, singleEvents=True).execute()
    events = eventsResult.get('items', [])
    if events:
        for x in events:
            cal_service.events().delete(calendarId=flask.session['calendar_id'], eventId=x['id']).execute()


    for x in list_in:
        if datetime.datetime.now() < datetime.datetime.strptime('06:00:00', '%H:%M:%S'):
            _date = datetime.date.today()
        else:
            _date = datetime.date.today() + datetime.timedelta(days=1)

        x[0] = (datetime.datetime.combine(_date, (datetime.datetime.min+x[0]).time())).isoformat()
        x[1] = (datetime.datetime.combine(_date, (datetime.datetime.min+x[1]).time())).isoformat()
        event = {
            'summary': 'Shower Time for '+ x[2] ,
            'description': 'Shower times optimized for you by 741 inc.',
            'start': {
                'dateTime': x[0],
                'timeZone': 'America/Detroit',
            },
            'end': {
                'dateTime': x[1],
                'timeZone': 'America/Detroit',
            },
            'reminders': {
                'useDefault': False
            },
        }

        credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
        http_auth = credentials.authorize(httplib2.Http())
        cal_service = discovery.build('calendar', 'v3', http_auth)
        event = cal_service.events().insert(calendarId=flask.session['calendar_id'], body=event).execute()


def run_algorithm(address_in):

    Users = get_user_events(address_in)

    """ 0 - username, 1 - event start, 2 - shower time, 3 - prefered time before event"""
    Users = convert_times(Users)
    outSchedule = calc_best(Users)

    write_calendar(outSchedule)


##################################################################################




@app.route('/')
@app.route('/main')
def main():
    return render_template("index.html")

@app.route('/home')
def home():
    if flask.session['signed_in']:
        return render_template('home.html')
    else:
        return render_template('index.html')


@app.route('/showSignUp')
@app.route('/showSignUp/<exists>')
def showSignUp(exists=None):
    return render_template('signup.html', exists=exists)

@app.route('/showSignIn')
def showSignIn(invalid=None):
    return render_template('signin.html', invalid=invalid)

@app.route('/signIn', methods=['POST'])
def signIn():
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']

    if _email and _password:
        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute("SELECT password FROM SmartShowerDB.users WHERE email='{0}'".format(_email))
        result = cursor.fetchall()
        pw = result[0][0]
        
        if (pw == _password):
            cursor.execute("SELECT id, fname, lname FROM SmartShowerDB.users WHERE email='{0}'".format(_email))
            result = cursor.fetchall()
            flask.session['last_id'] = result[0][0]
            flask.session['fname'] = result[0][1]
            flask.session['lname'] = result[0][2]
            flask.session['signed_in'] = True
#            return render_template('home.html') 
            return render_template('home.html')
        else:
            return render_template('signin.html', invalid=True)
    else:
        return render_template('signin.html', invalid=True)



@app.route('/signUp', methods=['POST'])
def signUp():
    #get data from submitted form
    _fname = request.form['inputFName']
    _lname = request.form['inputLName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']

    if _fname and _lname and _email and _password:

        #couldnt get mysql.connect() to work, ran into "Connection object is not callable"
        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute('''SELECT EXISTS(
			SELECT 1 
			FROM SmartShowerDB.users
			WHERE email = '{0}')'''.format(_email))
        result = cursor.fetchall();
        exists = result[0][0]
        
        if exists:
            return render_template('signup.html', exists=True);
        else:
            cursor.execute(''' INSERT INTO SmartShowerDB.users(
			fname,
			lname,
			email,
			password
		)
		VALUES(
                        '{0}',
			'{1}',
			'{2}',
			'{3}'
		);'''.format(_fname, _lname, _email, _password));
            conn.commit()
            cursor.execute("SELECT LAST_INSERT_ID()")
            result = cursor.fetchall()
            last_id = result[0][0]
            flask.session['last_id'] = last_id
            flask.session['fname'] = _fname
            flask.session['lname'] = _lname
            flask.session['signed_in'] = True
            return render_template('completeProfile.html', last_id=last_id)
    else:
        return json.dumps({'html':'<span>fields incorrect</span>'})

@app.route('/complete', methods=['POST'])
def complete():
    _phone = request.form['phone']
    _address = request.form['address']
    _ampm = request.form['ampm']
    _duration = request.form['duration']
    _buffer = request.form['buffer']
    _last_id = request.form['last_id']

    if _phone and _address and _ampm and _duration and _buffer:
        conn = mysql.connection
        cursor = conn.cursor()
        morning = 0
        if _ampm == 'am':
            morning = 1
        
        cursor.execute('''UPDATE SmartShowerDB.users
               SET phone = '{0}',
                   address = '{1}',
                   morning = '{2}',
                   duration = '{3}',
                   buffer = '{4}'
               WHERE id = '{5}';
                    '''.format(_phone, _address, morning, _duration, _buffer, _last_id));
        conn.commit()
        
        cursor.execute('''
			SELECT calendar_id 
			FROM SmartShowerDB.users
			WHERE address = '{0}'
                        AND calendar_id IS NOT NULL
                        '''.format(_address))
        result = cursor.fetchall()
        
        if result:
            _calendar_id = result[0][0]
            flask.session['calendar_id'] = _calendar_id

            cursor.execute('''UPDATE SmartShowerDB.users
                            SET calendar_id = '{0}'
                            WHERE id = '{1}';'''.format(_calendar_id, _last_id))
            conn.commit()
            return flask.redirect(flask.url_for('addSharedCalendar'))
        else:
            return flask.redirect(flask.url_for('createSharedCalendar'))
            #flask.session['calendar_id'] = None
        return render_template("addEarliest.html", last_id=_last_id)

    else:
        return json.dumps({'html':'<span>fields incorrect</span>'})

@app.route('/addSharedCalendar')
def addSharedCalendar():
    flask.session['oauth_caller'] = 'addSharedCalendar'

    if 'credentials' not in flask.session:
        return flask.redirect(flask.url_for('oauth2callback'))
    credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
    if credentials.access_token_expired:
        return flask.redirect(flask.url_for('oauth2callback'))
    else:
        http_auth = credentials.authorize(httplib2.Http())
        cal_service = discovery.build('calendar', 'v3', http_auth)

    calendar_id = flask.session['calendar_id']

    ##add to acl
    rule = {
        'scope': {
            'type': 'domain',
            'value': 'umich.edu'
        },
        'role': 'writer'
    }
    cal_service.acl().insert(calendarId=calendar_id, body=rule).execute()

    ##add to cal list
    calendar_list_entry = {
        'id': calendar_id
    }
    cal_service.calendarList().insert(body=calendar_list_entry).execute()

    uid = flask.session['last_id']
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute('''UPDATE SmartShowerDB.users
                SET calendar_id = '{0}'
                WHERE id = '{1}';'''.format(calendar_id, uid))
    conn.commit()
    return render_template("addEarliest.html", last_id=uid)    



@app.route('/createSharedCalendar')
def createSharedCalendar():
    flask.session['oauth_caller'] = 'createSharedCalendar'

    if 'credentials' not in flask.session:
        return flask.redirect(flask.url_for('oauth2callback'))
    credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
    if credentials.access_token_expired:
        return flask.redirect(flask.url_for('oauth2callback'))
    else:
        http_auth = credentials.authorize(httplib2.Http())
        cal_service = discovery.build('calendar', 'v3', http_auth)
    
    ##create calendar
    calendar = {
        'summary': 'SmartShower Schedule',
        'timeZone': 'America/Detroit'
    }

    created_calendar = cal_service.calendars().insert(body=calendar).execute()
    calendar_id = created_calendar['id']
    
    ##add to acl
    rule = {
        'scope': {
            'type': 'domain',
            'value': 'umich.edu'
        },
        'role': 'writer'
    }
    cal_service.acl().insert(calendarId=calendar_id, body=rule).execute()

    ##add to cal list
    calendar_list_entry = {
        'id': calendar_id
    }
    cal_service.calendarList().insert(body=calendar_list_entry).execute()

    uid = flask.session['last_id']
    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute('''UPDATE SmartShowerDB.users
                SET calendar_id = '{0}'
                WHERE id = '{1}';'''.format(calendar_id, uid))
    conn.commit()
    return render_template("addEarliest.html", last_id=uid)    

@app.route('/register', methods=['POST', 'GET'])
def register():
    flask.session['oauth_caller'] = 'register'

    if 'credentials' not in flask.session:
        return flask.redirect(flask.url_for('oauth2callback'))
    credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
    if credentials.access_token_expired:
        return flask.redirect(flask.url_for('oauth2callback'))
    else:
        http_auth = credentials.authorize(httplib2.Http())
        cal_service = discovery.build('calendar', 'v3', http_auth)

    if (datetime.datetime.utcnow() < datetime.datetime.strptime('06:00:00', '%H:%M:%S')):
        now = datetime.datetime.utcnow().isoformat() + 'Z'
        endOfDay = datetime.datetime.combine(datetime.date.today(), datetime.datetime.strptime('23:59:59', '%H:%M:%S').time()).isoformat() +'Z'
    else: 
        now = datetime.datetime.combine(datetime.date.today(), datetime.datetime.strptime('23:59:59', '%H:%M:%S').time()).isoformat() +'Z'
        endOfDay = datetime.datetime.combine(datetime.date.today()+datetime.timedelta(days=1), datetime.datetime.strptime('23:59:59', '%H:%M:%S').time()).isoformat() +'Z'
    eventsResult = cal_service.events().list(
        calendarId='primary', timeMin=now, timeMax=endOfDay, maxResults=1, singleEvents=True).execute()
    events = eventsResult.get('items', [])
    last_id = flask.session['last_id']
    conn = mysql.connection
    cursor = conn.cursor()
    if not events:
        #write null to db
        notice = "no events"
    else:
        start = events[0]['start'].get('dateTime')
        notice = start
        cursor.execute('''UPDATE SmartShowerDB.users
                SET event = '{0}'
                WHERE id = '{1}'
                '''.format(start, last_id))
    cursor.execute("SELECT address FROM smartshowerdb.users WHERE id = '{0}'".format(last_id))
    result = cursor.fetchall()
    address = result[0][0]
    run_algorithm(address)
    
    return notice


@app.route('/oauth2callback')
def oauth2callback():
    flow = client.flow_from_clientsecrets(
                CLIENT_SECRET_FILE,
                SCOPE,
                redirect_uri=flask.url_for('oauth2callback', _external=True)
                )
    if 'code' not in flask.request.args:
        auth_uri = flow.step1_get_authorize_url()
        return flask.redirect(auth_uri)
    else:
        auth_code = flask.request.args.get('code')
        credentials = flow.step2_exchange(auth_code)
        flask.session['credentials'] = credentials.to_json()
        caller = flask.session['oauth_caller']
        return flask.redirect(flask.url_for(caller))

if __name__ == "__main__":
    app.run(debug=True)


