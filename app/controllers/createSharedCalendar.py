from flask import *
from app import app, mysql
from flask import render_template
from flask import request, session
from flask import json
import json
from werkzeug import generate_password_hash, check_password_hash
from oauth2client import client
import httplib2
from apiclient import discovery
import datetime


createSharedCalendar = Blueprint('createSharedCalendar', __name__, template_folder='views')

@createSharedCalendar.route('/createSharedCalendar')
def create():
    session['oauth_caller'] = 'createSharedCalendar.create'

    if 'credentials' not in session:
        return redirect('/oauth2callback')
    credentials = client.OAuth2Credentials.from_json(session['credentials'])
    if credentials.access_token_expired:
        return redirect('/oauth2callback')
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

    uid = session['last_id']
    session['calendar_id'] = calendar_id

    conn = mysql.connection
    cursor = conn.cursor()
    ##cursor.execute('''UPDATE SmartShowerDB.users
    ##            SET calendar_id = '{0}'
    ##            WHERE id = '{1}';'''.format(calendar_id, uid))

    sql = "SELECT address FROM SmartShowerDB.users WHERE id = %s"
    cursor.execute(sql, (uid))
    _address = cursor.fetchall()[0][0] 

    sql = "UPDATE SmartShowerDB.address SET calendar_id = %s WHERE address = %s"
    cursor.execute(sql, (_address))

    conn.commit()
    return render_template("addEarliest.html", last_id=uid)  
