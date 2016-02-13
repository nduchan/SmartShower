from flask import *
from app import app, mysql
from flask import render_template
from flask import request, session
from flask import json
import json



signout = Blueprint('signout', __name__, template_folder='views')

@signout.route('/signout', methods=['GET'])
def logout():
	session.clear()
	return redirect('/home')