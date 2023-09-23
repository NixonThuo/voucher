from application import db

class Users(db.Model):
    __bind_key__ = 'maindb'
    __tablename__ = 'users'
    __table_args__ = {
        'autoload': True,
        'autoload_with': db.get_engine(bind="maindb")
    }
