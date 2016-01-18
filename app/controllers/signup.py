from flask import *
from app import app, mysql
from flask import render_template
from flask import request
from flask import json
import json


signup = Blueprint('signup', __name__, template_folder='views')


@signup.route('/signup', methods=['GET'])
def showSignUp(exists=None):
    return render_template('signup.html', exists=exists)

@signup.route('/signup', methods=['POST'])
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