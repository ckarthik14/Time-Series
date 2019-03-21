import MySQLdb
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, user_id, user_pass=None, user_name=None):
        self.user_id = user_id
        self.user_pass = user_pass
        self.user_name = user_name

    def get(uid):
        db = MySQLdb.connect('localhost','root','1','timeseries')
        cur = db.cursor()

        res = cur.execute("SELECT * FROM users WHERE user_id = %s", (uid,))

        if(res == 1):
            record = cur.fetchall()[0]

            db.close()
            
            user_id = record[0]
            user_pass = record[1]
            user_name = record[2]
            return User(user_id,user_pass,user_name)

        return None

    def check_authenticated(self, password):
        db = MySQLdb.connect('localhost','root','1','timeseries')
        cur = db.cursor()
        
        if(self.user_pass == str(password)):
            return True

        return False
    
    def get_id(self):
        return self.user_id.encode('utf-8')
