#import MySQLdb
import MySQLdb
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, user_id, user_email=None, user_pass=None, user_affiliation=None):
        self.user_id = user_id
        self.user_email = user_email
        self.user_pass = user_pass
        self.user_affiliation = user_affiliation

    def get(uid):
        db = MySQLdb.connect('localhost','root','1','timeseries')
        cur = db.cursor()

        res = cur.execute("SELECT * FROM users WHERE user_email = %s", (uid,))

        if(res == 1):
            record = cur.fetchall()[0]

            db.close()
            
            user_id = record[0]
            user_email = record[1]
            user_pass = record[2]
            user_affiliation = record[3]
            return User(user_id,user_email,user_pass,user_affiliation)

        return None

    def check_authenticated(self, password):
        
        if(self.user_pass == str(password)):
            return True

        return False
    
    def get_id(self):
        return self.user_email.encode('utf-8')
