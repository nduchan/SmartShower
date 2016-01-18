from flask import *
from flask.ext.mysqldb import MySQL
from flask import render_template

main = Blueprint('main', __name__, template_folder='views')


@main.route('/')
@main.route('/main')
def display_main():
    return render_template("index.html")