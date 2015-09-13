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

@app.route('/')
@app.route('/main')
def main():
    return render_template("index.html")

@app.route('/showSignUp')
@app.route('/showSignUp/<exists>')
def showSignUp(exists=None):
    return render_template('signup.html', exists=exists)

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
        _hashed_password = generate_password_hash(_password)
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
		);'''.format(_fname, _lname, _email, _hashed_password));
            conn.commit()
            cursor.execute("SELECT LAST_INSERT_ID()")
            result = cursor.fetchall()
            last_id = result[0][0]
            print last_id
            flask.session['last_id'] = last_id
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
        morning = False
        if _ampm == 'am':
            morning = True
        cursor.execute('''UPDATE SmartShowerDB.users
               SET phone = '{0}',
                   address = '{1}',
                   morning = '{2}',
                   duration = '{3}',
                   buffer = '{4}'
               WHERE id = '{5}';
                    '''.format(_phone, _address, morning, _duration, _buffer, _last_id));
        conn.commit()
        return render_template("addEarliest.html", last_id=_last_id)

    else:
        return json.dumps({'html':'<span>fields incorrect</span>'})

@app.route('/register', methods=['POST', 'GET'])
def register():
    if 'credentials' not in flask.session:
        return flask.redirect(flask.url_for('oauth2callback'))
    credentials = client.OAuth2Credentials.from_json(flask.session['credentials'])
    if credentials.access_token_expired:
        return flask.redirect(flask.url_for('oauth2callback'))
    else:
        http_auth = credentials.authorize(httplib2.Http())
        cal_service = discovery.build('calendar', 'v3', http_auth)

        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        eventsResult = cal_service.events().list(
            calendarId='primary', timeMin=now, maxResults=1, singleEvents=True,
            orderBy='startTime').execute()
        events = eventsResult.get('items', [])
        if not events:
            #write null to db
            return "no events"
        else:
            last_id = flask.session['last_id']
            start = events[0]['start'].get('dateTime')
            conn = mysql.connection
            cursor = conn.cursor()
            cursor.execute('''UPDATE SmartShowerDB.users
                    SET event = '{0}'
                    WHERE id = '{1}'
                    '''.format(start, last_id)) 
            return start


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
        return flask.redirect(flask.url_for('register'))

if __name__ == "__main__":
    app.run(debug=True)




