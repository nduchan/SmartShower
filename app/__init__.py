from flask import Flask, render_template
from flask.ext.mysqldb import MySQL

app = Flask(__name__, template_folder='views', static_folder='static')

# app.config.from_object('config')

print "making msql and app"
mysql = MySQL()

DATABASE_NAME = 'SmartShowerDB'
# Stuff for DB Configuration
# app.config['MYSQL_USER'] = 'group74'
# app.config['MYSQL_PASSWORD'] = 'paddlepals'

app.config['DEBUG'] = True
mysql.init_app(app)

app.config['MYSQL_USER'] = 'root'


import controllers
app.register_blueprint(controllers.home)
app.register_blueprint(controllers.main)
app.register_blueprint(controllers.signin)
app.register_blueprint(controllers.signup)
