from flask import *
from app import app, mysql
from flask import render_template
from flask import request, session
from flask import json
import json



signin = Blueprint('signin', __name__, template_folder='views')

@signin.route('/signin', methods=['GET'])
def display_signin():
    return render_template('signin.html')

@signin.route('/signin', methods=['POST'])
def signIn():
    _email = request.form['inputEmail']
    _password = request.form['inputPassword']

    if _email and _password:
        conn = mysql.connection
        cursor = conn.cursor()

        sql = "SELECT password FROM SmartShowerDB.users WHERE email='%s'" % _email
        num_found = cursor.execute(sql)
        if num_found == 0:
            return render_template('signin.html', invalid=True)
        result = cursor.fetchall()
        pw = result[0][0]
        
        if (pw == _password):
<<<<<<< HEAD
            sql = "SELECT (id, fname, lname) FROM SmartShowerDB.users WHERE email=%s"
            cursor.execute(sql, _email)
=======
            print _email
            sql = "SELECT id, fname, lname FROM SmartShowerDB.users WHERE email='%s'" % _email
            print sql
            cursor.execute(sql)
>>>>>>> origin/master
            result = cursor.fetchall()
            session['last_id'] = result[0][0]
            session['fname'] = result[0][1]
            session['lname'] = result[0][2]
            session['signed_in'] = True
            return render_template('home.html')
        else:
            return render_template('signin.html', invalid=True)
    else:
        return render_template('signin.html', invalid=True)
