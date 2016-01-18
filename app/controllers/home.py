@app.route('/home')
def home():
    if flask.session['signed_in']:
        return render_template('home.html', calendar_id=json.dumps(calendar_id))
    else:
        return render_template('index.html')