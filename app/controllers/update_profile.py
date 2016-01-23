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
        return redirect(url_for('signIn'))

    return render_template('completeProfile.html', last_id=last_id)



@update_profile.route('/update_profile', methods=['POST'])
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
        

        sql = "UPDATE SmartShowerDB.users SET (phone=%d, address=%s, morning=%s, duration=%i, buffer=%i) WHERE id=%i"

        cursor.execute(sql, (_phone, _address, morning, _duration, _buffer, _last_id))
        conn.commit()
        
        cursor.execute("SELECT calendar_id FROM SmartShowerDB.users WHERE address = _address AND calendar_id IS NOT NULL")
        result = cursor.fetchall()
        
        if result:
            _calendar_id = result[0][0]
            session['calendar_id'] = _calendar_id

            cursor.execute('''UPDATE SmartShowerDB.users
                            SET calendar_id = '{0}'
                            WHERE id = '{1}';'''.format(_calendar_id, _last_id))
            conn.commit()
            return redirect('/addSharedCalendar')
        else:
            #will need this line
            return redirect('/createSharedCalendar')
            #flask.session['calendar_id'] = None

    else:
        return json.dumps({'html':'<span>fields incorrect</span>'})