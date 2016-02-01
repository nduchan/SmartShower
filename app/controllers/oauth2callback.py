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

CLIENT_ID = "456555048105-49j7n97kvjuluk4f0b3598m70sk0e293"
SCOPE = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'SmartShower'

oauth2callback = Blueprint('oauth2callback', __name__, template_folder='views')


@oauth2callback.route('/oauth2callback')
def oauth():
    flow = client.flow_from_clientsecrets(
                CLIENT_SECRET_FILE,
                SCOPE,
                redirect_uri=url_for('oauth2callback.oauth', _external=True)
                )
    if 'code' not in request.args:
        auth_uri = flow.step1_get_authorize_url()
        print "=============AUTH_URI = %s", auth_uri
        return redirect(auth_uri)
    else:
        auth_code = request.args.get('code')
        credentials = flow.step2_exchange(auth_code)
        session['credentials'] = credentials.to_json()
        caller = session['oauth_caller']
        print "%s", caller
        return redirect(url_for(caller))