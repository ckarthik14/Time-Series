from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_login import LoginManager, login_user, login_required, current_user
from random import sample
from userclass import User

app = Flask(__name__)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['LOGIN_DISABLED'] = False

login_manager = LoginManager()
login_manager.init_app(app)

@app.route('/')
def hello_world():
    return render_template('charts.html')

@app.route('/data')
def data():
    return jsonify({'results':sample(range(1,20),10)})

@login_manager.user_loader
def user_loader(email):
    print('in user_loader')
    return User.get(uid=email)

@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.get(uid=email)

    print('in request_loader')

    if(user == None):
        return None
    
    if(user.check_authenticated(password=password)):
        user.is_authenticated = True

    return user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return '''
               <form action='login' method='POST'>
                <input type='text' name='email' id='email' placeholder='email'/>
                <input type='password' name='password' id='password' placeholder='password'/>
                <input type='submit' name='submit'/>
               </form>
               '''

    email = request.form['email']
    password = request.form['password']
    user = User.get(uid=email)
    print(user.is_authenticated)
    if user != None and user.check_authenticated(password=password):
        print('in login')
        login_user(user)
        return redirect(url_for('protected'))

    return 'Bad login'


@app.route('/protected')
@login_required
def protected():
    return 'Logged in as: ' + current_user.user_name

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'

if __name__ == '__main__':
    app.run(port=9999)
