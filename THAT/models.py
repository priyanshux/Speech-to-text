from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from THAT import db,login_manager,application
from flask_login import UserMixin

#decorator for login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) #getting user by id


class User(db.Model, UserMixin):
    #__tablename__ = "users"
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(20),unique=True, nullable=False)
    email=db.Column(db.String(100),unique=True, nullable=False)
    password=db.Column(db.String(50),nullable=False)
    lectures=db.relationship('Lecture',backref='author',lazy=True)

    def __repr__(self):
        return f"User('{self.username}','{self.email}')"

class Lecture(db.Model):
    #__tablename__ = "lectures"
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100), nullable=False)
    date=db.Column(db.Date(),nullable=False)
    starttime=db.Column(db.Time,nullable=True)
    endtime=db.Column(db.Time,nullable=True)
    details=db.Column(db.Text,nullable=True)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    def __repr__(self):
        return f"Lecture('{self.title}','{self.date}','{self.starttime}','{self.endtime}',{self.status}')"


