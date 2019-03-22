from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from random import sample
from userclass import User

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['LOGIN_DISABLED'] = False

login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/')
@login_required
def hello_world():
    return render_template('charts.html')

@app.route('/data')
@login_required
def data():
    return jsonify({'results':sample(range(1,20),10)})

@login_manager.user_loader
def user_loader(email):
    return User.get(uid=email)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    email = request.form['email']
    password = request.form['password']
    user = User.get(uid=email)
    print(user.is_authenticated)
    if user != None and user.check_authenticated(password=password):
        login_user(user)
        return redirect('/')

    flash('Invalid Login')

    return redirect(url_for('login'))


@app.route('/protected')
@login_required
def protected():
    return 'Logged in as: ' + current_user.user_id + "<form action='/logout'><button onclick='this.form.submit();'> Logout </form>"

@app.route('/logout')
def logout():
    logout_user()
    return 'Logged out'

@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=9999)
