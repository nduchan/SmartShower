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


createSharedCalendar = Blueprint('createSharedCalendar', __name__, template_folder='views')

@createSharedCalendar.route('/createSharedCalendar')
def create():
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
    flask.session['calendar_id'] = calendar_id

    conn = mysql.connection
    cursor = conn.cursor()
    cursor.execute('''UPDATE SmartShowerDB.users
                SET calendar_id = '{0}'
                WHERE id = '{1}';'''.format(calendar_id, uid))
    conn.commit()
    return render_template("addEarliest.html", last_id=uid)  