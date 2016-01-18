from flask import *
from app import app
from flask.ext.mysqldb import MySQL
from flask import render_template

main = Blueprint('main', __name__, template_folder='views')


@main.route('/')
@main.route('/main')
def main():
    return render_template("index.html")