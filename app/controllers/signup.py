from flask import *
from app import app, mysql
from flask import render_template
from flask import request, session
from flask import json
import json

signup = Blueprint('signup', __name__, template_folder='views')

@signup.route('/signup', methods=['GET'])
def showSignUp():
    return render_template('signup.html', exists=None)

@signup.route('/signup', methods=['POST'])
def signUp():
    #get data from submitted form
    _fname = request.form['inputFName']
    _lname = request.form['inputLName']
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']
    _address = request.form['inputAddress']

    if _fname and _lname and _email and _password and _address:

        conn = mysql.connection
        cursor = conn.cursor()
        sql = "SELECT EXISTS(SELECT 1 FROM SmartShowerDB.users WHERE email='%s')" % _email
        cursor.execute(sql)
        result = cursor.fetchall();
        exists = result[0][0]
        
        if exists:
            return render_template('signup.html', exists=True);
        else:
            sql = "INSERT INTO SmartShowerDB.users (fname, lname, email, password, address) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (_fname, _lname, _email, _password, _address))
            conn.commit()
            cursor.execute("SELECT LAST_INSERT_ID()")
            result = cursor.fetchall()
            last_id = result[0][0]
            session['last_id'] = last_id
            session['fname'] = _fname
            session['lname'] = _lname
            session['signed_in'] = True
            session['address'] = _address
            #return render_template('completeProfile.html', last_id=last_id)
            return redirect('/update_profile')

    else:
        return json.dumps({'html':'<span>fields incorrect</span>'})