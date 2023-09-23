from application import db, login_manager
from datetime import datetime
import hashlib


class Users(db.Model):
    __tablename__ = 'users'
    userid = db.Column(
        'user_id', db.Integer, primary_key=True)
    username = db.Column('username', db.String)
    useremail = db.Column('user_email', db.String)
    password = db.Column('password', db.String)
    dateadded = db.Column('date_added', db.Date, default=datetime.now())
    isenabled = db.Column('isenabled', db.Boolean, default=True)
    isactive = True
    isanonymous = False
    authenticated = False

    def password_check(self, password):
        print(self.password)
        print(hashlib.md5(password.encode()).hexdigest())
        if self.password == hashlib.md5(password.encode()).hexdigest():
            print("passwords match")
            return True
        else:
            return False

    def set_is_authenticated(self, isauthenticated):
        self.authenticated = isauthenticated

    def is_active(self):
        return self.isactive

    def is_anonymous(self):
        return self.isanonymous

    def get_id(self):
        return str(self.userid).encode("utf").decode("utf-8")


@login_manager.user_loader
def load_user(userid):
    try:
        return Users.query.get(int(userid))
    except ValueError as e:
        return None
