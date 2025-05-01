from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from app import db

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    password_hash = db.Column(db.String(1024), nullable=False)
    team = db.Column(db.String(64), nullable=False)  # Admin, Devops, HR, Visitor

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    teamName = db.Column(db.String(64), nullable=False, unique=True)

    def __repr__(self):
        return f'<Team {self.teamName}>'

class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True,nullable=False, unique=True)
    roomName = db.Column(db.String(64), nullable=False)
    telephone = db.Column(db.Boolean, nullable=False)
    projector = db.Column(db.Boolean, nullable=False)
    whiteboard = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f'Room {self.roomName}'

class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True,nullable=False, unique=True)
    title = db.Column(db.String(64), nullable=False, unique=True)
    teamId = db.Column(db.Integer, db.ForeignKey('team.id'))
    roomId = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    bookerId = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.Date, nullable=False)  # Changed from db.DateTime to db.Date
    startTime = db.Column(db.Integer, nullable=False)
    endTime = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'Meeting {self.title}'

class Participants_user(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True)
    meeting = db.Column(db.String(64), db.ForeignKey('meeting.title'))
    userId = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<Participants_user meeting={self.meeting}, userId={self.userId}>'




