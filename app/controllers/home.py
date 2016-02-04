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
    	if session['signed_in']:
    		print "rendering home.html"
        	return render_template('home.html', calendar_id=json.dumps(calendar_id))
    	else:
        	return render_template('index.html')
    except:
    	print "rendering index.html"
    	return render_template('index.html')