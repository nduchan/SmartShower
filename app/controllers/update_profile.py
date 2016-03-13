from flask import *
from app import app, mysql
from flask import render_template
from flask import request, session
from flask import json
import json

update_profile = Blueprint('update_profile', __name__, template_folder='views')

@update_profile.route('/update_profile', methods=['GET'])
def update():
    if "last_id" in session:
        last_id = session['last_id']
    else:
        return redirect('/signin')

    return render_template('completeProfile.html', last_id=last_id)



@update_profile.route('/update_profile', methods=['POST'])
def complete():

    # if request.method == 'GET':
    #     if "last_id" in session:
    #         last_id = session['last_id']
    #     else:
    #        return redirect('/signin')
    #     return render_template('completeProfile.html', last_id=last_id)

    _address = session['address']
    _phone = request.form['phone']
    _ampm = request.form['ampm']
    _duration = request.form['duration']
    _buffer = request.form['buffer']

    if 'signed_in' in session:
        if session['signed_in'] == False:
            print "User signedin is false try logging in"
            return redirect('/signin')
        else:
            _last_id = session["last_id"]

    else:
        print "User not signed in, try logging in first!"
        return redirect('/signin')

    if _phone and _ampm and _duration and _buffer:
        conn = mysql.connection
        cursor = conn.cursor()
        morning = 0
        if _ampm == 'am':
            morning = 1
        

        sql = "UPDATE SmartShowerDB.users SET phone=%s, morning=%s, duration=%s, buffer=%s WHERE id=%s"

        cursor.execute(sql, (_phone, morning, _duration, _buffer, _last_id))
        conn.commit()
        print "address = " + address
        cursor.execute("SELECT calendar_id FROM SmartShowerDB.address WHERE address = %s AND calendar_id IS NOT NULL" , (_address))
        result = cursor.fetchall()
        
        if result:
            _calendar_id = result[0][0]
            session['calendar_id'] = _calendar_id

            return redirect('/addSharedCalendar')
        else:
            #will need this line
            return redirect('/createSharedCalendar')
            #flask.session['calendar_id'] = None

    else:
        return json.dumps({'html':'<span>fields incorrect</span>'})