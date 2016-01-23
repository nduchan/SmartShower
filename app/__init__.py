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

app.secret_key = '\xae\x0e\x1a\xb5\x1e@\xf1\x8e\xd4\xfb\x9c\xe08Z\xd7\xf4\x0c\xe4\x97\xe7\x9c\x14\xc8\xd1'


import controllers
app.register_blueprint(controllers.home)
app.register_blueprint(controllers.main)
app.register_blueprint(controllers.signin)
app.register_blueprint(controllers.signup)
app.register_blueprint(controllers.update_profile)
#app.register_blueprint(controllers.createSharedCalendar)

