from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DateField, SelectMultipleField, widgets
from wtforms.validators import ValidationError, DataRequired, EqualTo
from flask_login import current_user
from app.models import *

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    team = SelectField('Team', choices=[('Admin', 'Admin'), ('Devops', 'Devops'), ('HR', 'HR'), ('Visitor', 'Visitor')], validators=[DataRequired()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=self.username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

class AddteamForm(FlaskForm):
    teamName = StringField('Team name', validators=[DataRequired()])
    submit = SubmitField('Add Team')

    def validate_teamName(self, teamName):
        team = Team.query.filter_by(teamName=teamName.data).first()
        if team is not None:
            raise ValidationError('Team name already exists.')

class AdduserForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    team = SelectField('Team', choices=[('Admin', 'Admin'), ('Devops', 'Devops'), ('HR', 'HR'), ('Visitor', 'Visitor')], validators=[DataRequired()])
    submit = SubmitField('Add User')

    def validate_username(self, username):
        user = User.query.filter_by(username=self.username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

class DeleteteamForm(FlaskForm):
    teamName = SelectField('Choose Team', validators=[DataRequired()])
    submit = SubmitField('Delete Team')

    def __init__(self, *args, **kwargs):
        super(DeleteteamForm, self).__init__(*args, **kwargs)
        self.teamName.choices = [(team.teamName, team.teamName) for team in Team.query.all()]

class DeleteuserForm(FlaskForm):
    username = SelectField('Choose User', validators=[DataRequired()])
    submit = SubmitField('Delete User')

    def __init__(self, *args, **kwargs):
        super(DeleteuserForm, self).__init__(*args, **kwargs)
        self.username.choices = [(user.username, user.username) for user in User.query.all()]

class BookmeetingForm(FlaskForm):
    title = StringField('Meeting Title', validators=[DataRequired()])
    room = SelectField('Choose Room', coerce=int, validators=[DataRequired()])
    date = DateField('Choose Date', format="%Y-%m-%d", validators=[DataRequired(message="Please select a valid date.")])
    startTime = SelectField('Start Time (24hr)', choices=[(i, i) for i in range(9, 19)], coerce=int, validators=[DataRequired()])
    endTime = SelectField('End Time (24hr)', choices=[(i, i) for i in range(10, 20)], coerce=int, validators=[DataRequired()])
    submit = SubmitField('Book Meeting')

    def __init__(self, *args, **kwargs):
        super(BookmeetingForm, self).__init__(*args, **kwargs)
        self.room.choices = [(room.id, room.roomName) for room in Room.query.all()]

    def validate_title(self, title):
        meeting = Meeting.query.filter_by(title=self.title.data).first()
        if meeting is not None:
            raise ValidationError('Please use a different meeting title.')

    def validate_endTime(self, endTime):
        if self.endTime.data <= self.startTime.data:
            raise ValidationError('End time must be after start time.')

class CancelbookingForm(FlaskForm):
    ids = SelectField('Meeting ID', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Cancel Booking')

    def __init__(self, *args, **kwargs):
        super(CancelbookingForm, self).__init__(*args, **kwargs)
        self.ids.choices = [(meeting.id, meeting.title) for meeting in Meeting.query.all()]

class RoomavailableForm(FlaskForm):
    date = DateField('Choose Date', format="%Y-%m-%d", validators=[DataRequired(message="Please select a valid date.")])
    startTime = SelectField('Start Time (24hr)', choices=[(i, i) for i in range(9, 19)], coerce=int, validators=[DataRequired()])
    duration = SelectField('Duration (hours)', choices=[(i, i) for i in range(1, 5)], coerce=int, validators=[DataRequired()])
    submit = SubmitField('Check Availability')

class RoomoccupationForm(FlaskForm):
    date = DateField('Choose Date', format="%Y-%m-%d", validators=[DataRequired(message="Please select a valid date.")])
    submit = SubmitField('Check Room Occupation')

class MeetingparticipantsForm(FlaskForm):
    ids = SelectField('Meeting ID', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Check Participants')

    def __init__(self, *args, **kwargs):
        super(MeetingparticipantsForm, self).__init__(*args, **kwargs)
        self.ids.choices = [(meeting.id, meeting.title) for meeting in Meeting.query.all()]