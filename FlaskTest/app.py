from flask import Flask, render_template,jsonify, request, redirect, url_for
from random import sample
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from userclass import User
import MySQLdb
app = Flask(__name__)

#SQL DB Connection
host = "localhost"
port = 3306
dbname = "timeseries"
user = "root"
password = "1"
connectionObject = MySQLdb.connect(host, user=user, port=port, passwd=password, db=dbname)

app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['LOGIN_DISABLED'] = False

login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/',methods = ["GET","POST"])
@login_required
def search_page():
    if(request.method == 'POST'):
        search_text =request.form['search_text']
    else:
        search_text = ''
    try:
         cursorObject = connectionObject.cursor()
         cursorObject.execute("select id from compressed_pages where pageName = %s",(search_text,))
         corresponding_pageID = cursorObject.fetchone()
         if(corresponding_pageID!= None):
            print(corresponding_pageID[0])
    except Exception as e:
        print("Inside Exception")
        print("Exeception occured:{}".format(e))

    #finally:
    #     connectionObject.close()
    print (search_text)
    cursor1 = connectionObject.cursor()
    cursor1.execute("select pageName from compressed_pages")
    page = cursor1.fetchall()
    return render_template('popups.html',pages = page)

@app.route('/data')
@login_required
def data():
    return jsonify({'results':sample(range(1,20),10)})

@login_manager.user_loader
def user_loader(email):
    print('in user_loader')
    return User.get(uid=email)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    affiliation = request.form['affiliation']
    email = request.form['email']
    password = request.form['password']

    cur = connectionObject.cursor()

    cur.execute('INSERT INTO users(user_email, password, affiliation) VALUES (%s,%s,%s)',(email,password,affiliation,))

    cur.execute('SELECT user_id from users WHERE user_email = %s', (email,))

    record = cur.fetchone()

    # @Kshitij, here is your ID
    user_id = record[0]
    
    connectionObject.close()

    return redirect(url_for('register'))
    
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    email = request.form['email']
    password = request.form['password']
    user = User.get(uid=email)
    
    if user != None and user.check_authenticated(password=password):
        login_user(user)
        return redirect('/')

    return 'Bad login'


@app.route('/protected')
@login_required
def protected():
    return 'Logged in as: ' + current_user.user_id + "<form action='/logout'><button onclick='this.form.submit();'> Logout </form>"

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return 'Logged out'

@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(port=9999)
