import flask
from flask import Flask
from flask.ext.mysqldb import MySQL
from flask import render_template

@app.route('/')
@app.route('/main')
def main():
    return render_template("index.html")