from flask import *
from app import app, mysql
from flask import render_template
from flask import request, session
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
		conn = mysql.connection
		cursor = conn.cursor()

		sql = "SELECT calendar_id FROM SmartShowerDB.users WHERE id='%s'" % session['last_id']
		num_found = cursor.execute(sql)
		if num_found == 0:
			#might need to be NULL or negavtive?
			calendar_id = 0
		else:
			calendar_id = cursor.fetchall()[0][0]
		session['calendar_id'] = calendar_id
		return render_template('home.html', calendar_id=session['calendar_id'])
	else:
		print "rendering index.html"
		return render_template('index.html')