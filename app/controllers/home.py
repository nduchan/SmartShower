import flask
from flask import *
from flask.ext.mysqldb import MySQL
from flask import render_template
from flask import json
import json

home = Blueprint('home', __name__, template_folder='views')

@home.route('/home')
def display_home():
	try:
		logged_in = session['signed_in']
	except:
		logged_in = False

	if logged_in == True:
		print "need CALENDAR_ID THEN SHOULD LOAD"
		return render_template('home.html', calendar_id=json.dumps(calendar_id))
	else:
		print "rendering index.html"
		return render_template('index.html')