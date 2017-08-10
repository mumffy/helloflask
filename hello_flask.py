from flask import Flask, url_for, request, render_template, session, redirect, flash
app = Flask(__name__)
app.secret_key = '\xa5\xc0\xda\xda\xa1\x14\xb4O\x0e\xca\xa7b\xac\xad%a@@\x9eG}\xb8\xa6\x1c'

class keys(object):
    logged_in = "logged_in"

@app.route('/<werd>')
def hello_world(werd):
    return "hello {0}".format(werd)

@app.route('/apple/<name>')
@app.route('/static/')
@app.route('/static')
def apple(name=None):
    return render_template('apple.html', name=name)

@app.route('/banana')
def banana():
    return "banana"

@app.route('/index/')
def index():
    return render_template('index.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            password = request.form['password']
            if "secret".upper() in str(password).upper():
                session[keys.logged_in] = True
                app.logger.info("user has logged in")
                flash("correct password")
            else:
                flash("incorrect password")
        except KeyError:
            password = None
            flash('password was not supplied')
            return redirect('logout')

        return redirect('index')
    # GET request
    else:
        return render_template('login.html')

@app.route('/logout/')
def logout():
    session.pop(keys.logged_in)
    app.logger.info("user has logged out")
    return redirect('index')