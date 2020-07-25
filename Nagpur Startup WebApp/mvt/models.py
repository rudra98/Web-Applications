from datetime import datetime
from mvt import db, login_manager
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='/static/profile_pics/default.jpg')
    password = db.Column(db.String(60), nullable=False)
    events = db.relationship('Events', backref='username', lazy=True)
    confirmed = db.Column(db.Boolean(), nullable=False, default=False)

    def __repr__(self):
        return "User('{self.username}', '{self.email}', '{self.image_file}')"


class Events(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    eventname = db.Column(db.String(20), unique=True, nullable=False)
    eventlocation = db.Column(db.String(120), nullable=False)
    eventdate = db.Column(db.DateTime, nullable=False)
    #image_file = db.Column(db.String(20), nullable=False, default='/static/eventpics/default.jpg')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)   
    

    def __repr__(self):
        return "Events('{self.eventdate}', '{self.eventname}', '{self.eventlocation}')"


       