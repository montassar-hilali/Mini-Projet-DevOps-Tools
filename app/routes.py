from flask import render_template, flash, redirect, request, url_for
from urllib.parse import urlparse  
from app import app
from app.forms import *
from flask_login import current_user, login_user, logout_user, login_required
from app.models import *
from app import db
import sqlite3
from authlib.integrations.flask_client import OAuth
from flask import session, jsonify

oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=app.config['OAUTH_CLIENT_ID'],
    client_secret=app.config['OAUTH_CLIENT_SECRET'],
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'openid email profile'}
)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page=request.args.get('next')
        if not next_page or urlparse(next_page).netloc!='':
            next_page=url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/login/oauth')
def login_oauth():
    redirect_uri = app.config['OAUTH_REDIRECT_URI']
    return google.authorize_redirect(redirect_uri)

@app.route('/oauth/callback')
def oauth_callback():
    token = google.authorize_access_token()
    user_info = google.get('userinfo').json()
    if user_info:
        session['user'] = user_info
        flash(f"Welcome, {user_info['name']}!")
        return redirect(url_for('index'))
    flash('Authentication failed.')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    # Handle Flask-Login logout
    if current_user.is_authenticated:
        logout_user()
    
    # Handle OAuth session logout
    if 'user' in session:
        session.pop('user', None)
    
    flash('You have been logged out.')
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        team = Team.query.filter_by(teamName=form.team.data).first()
        if not team:
            flash('Selected team does not exist.')
            return redirect(url_for('register'))
        user = User(username=form.username.data, team=team.teamName)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/adduser', methods=['GET', 'POST'])
@login_required
def adduser():
    if current_user.team != 'Admin':
        flash('Only admins can add users.')
        return redirect(url_for('index'))
    form = AdduserForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, team=form.team.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f'User {form.username.data} successfully added!')
        return redirect(url_for('adduser'))
    return render_template('adduser.html', title='Add User', form=form)

@app.route('/addteam', methods=['GET', 'POST'])
@login_required
def addteam():
    if current_user.team != 'Admin':
        flash('Only admins can add teams.')
        return redirect(url_for('index'))
    form = AddteamForm()
    if form.validate_on_submit():
        existing_team = Team.query.filter_by(teamName=form.teamName.data).first()
        if existing_team:
            flash(f'Team {form.teamName.data} already exists.')
            return redirect(url_for('addteam'))
        team = Team(teamName=form.teamName.data)
        db.session.add(team)
        db.session.commit()
        flash(f'Team {form.teamName.data} successfully added!')
        return redirect(url_for('addteam'))
    return render_template('addteam.html', title='Add Team', form=form)
        
@app.route('/deleteteam', methods=['GET', 'POST'])
@login_required
def deleteteam():
    if current_user.team != 'Admin':
        flash('Only admins can delete teams.')
        return redirect(url_for('index'))
    form = DeleteteamForm()
    if form.validate_on_submit():
        team = Team.query.filter_by(teamName=form.teamName.data).first()
        if team:
            db.session.delete(team)
            db.session.commit()
            flash(f'Team {form.teamName.data} successfully deleted!')
        else:
            flash('Team not found.')
        return redirect(url_for('deleteteam'))
    return render_template('deleteteam.html', title='Delete Team', form=form)

@app.route('/deleteuser', methods=['GET', 'POST'])
@login_required
def deleteuser():
    if current_user.team != 'Admin':
        flash('Only admins can delete users.')
        return redirect(url_for('index'))
    form = DeleteuserForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            flash(f'User {form.username.data} successfully deleted!')
        else:
            flash('User not found.')
        return redirect(url_for('deleteuser'))
    return render_template('deleteuser.html', title='Delete User', form=form)

@app.route('/book', methods=['GET', 'POST'])
@login_required
def book():
    form = BookmeetingForm()
    if form.validate_on_submit():
        # Check if the team exists
        team = Team.query.filter_by(id=current_user.id).first()
        if not team:
            flash('The team associated with your account does not exist.')
            return redirect(url_for('book'))

        # Check for time conflicts
        meetingcollisions = Meeting.query.filter_by(date=form.date.data, roomId=form.room.data).all()
        for meeting in meetingcollisions:
            if form.startTime.data < meeting.endTime and form.endTime.data > meeting.startTime:
                flash(f'Time conflict: {meeting.title} is already booked from {meeting.startTime} to {meeting.endTime}.')
                return redirect(url_for('book'))

        # Create the meeting
        meeting = Meeting(
            title=form.title.data,
            teamId=current_user.id,
            roomId=form.room.data,
            bookerId=current_user.id,
            date=form.date.data,  # Ensure this is a datetime.date object
            startTime=form.startTime.data,
            endTime=form.endTime.data
        )
        db.session.add(meeting)
        db.session.commit()
        flash('Meeting successfully booked!')
        return redirect(url_for('index'))
    return render_template('book.html', title='Book Meeting', form=form)

@app.route('/cancelbooking', methods=['GET', 'POST'])
@login_required
def cancelbooking():
    form = CancelbookingForm()
    if form.validate_on_submit():
        meeting = Meeting.query.filter_by(id=form.ids.data).first()
        if meeting and meeting.date > datetime.now().date():
            db.session.delete(meeting)
            db.session.commit()
            flash(f'Meeting {meeting.title} successfully canceled!')
        else:
            flash('Meeting not found or cannot cancel past meetings.')
        return redirect(url_for('cancelbooking'))
    return render_template('cancelbooking.html', title='Cancel Meeting', form=form)

@app.route('/roomavailable',methods=['GET','POST'])
def roomavailable():
    form=RoomavailableForm()
    if form.validate_on_submit():
        meetings=Meeting.query.filter_by(date=datetime.combine(form.date.data,datetime.min.time())).all()
        roomsOccupied = set()
        for meeting in meetings:
            if form.startTime.data < meeting.endTime and (form.startTime.data + form.duration.data) > meeting.startTime:
                roomsOccupied.add(meeting.roomId)
        rooms = Room.query.all()
        roomsavailable = []
        for room in rooms:
            if room.id not in roomsOccupied:
                roomsavailable.append(room)
        return render_template('roomavailablelist.html',title='Room available',rooms=roomsavailable)
    return render_template('roomavailable.html',title='Room availability check',form=form)

@app.route('/meetingbooker')
def meetingbooker():
    meetings=Meeting.query.order_by(Meeting.date).all()
    meetingreturns=[]
    for meeting in meetings:
        meetingreturn=dict()
        meetingreturn['title']=meeting.title
        meetingreturn['team']=Team.query.filter_by(id=meeting.teamId).first().teamName
        meetingreturn['room']=Room.query.filter_by(id=meeting.roomId).first().roomName
        meetingreturn['booker']=User.query.filter_by(id=meeting.bookerId).first().username
        meetingreturn['date']=meeting.date
        meetingreturn['time']=f'{meeting.startTime} to {meeting.endTime}'
        meetingreturns.append(meetingreturn)
    return render_template('meetingbooker.html',meetings=meetingreturns)



@app.route('/costs',methods=['GET','POST'])
def costs():
    form=CostaccruedForm()
    if form.validate_on_submit():
        costlogs=CostLog.query.filter(CostLog.date>=datetime.combine(form.startdate.data,datetime.min.time())).filter(CostLog.date<=datetime.combine(form.enddate.data,datetime.min.time())).all()
        teams=list(set([costlog.teamName for costlog in costlogs]))
        teamcosts=[]
        # slow implementation, can be optimized
        for team in teams:
            teamcost=dict()
            teamcost['teamName']=team
            teamcost['total']=0
            for costlog in costlogs:
                if costlog.teamName==team:
                    teamcost['total']+=costlog.cost
            teamcosts.append(teamcost)
        return render_template('costs.html',title='Cost Accrued',startdate=form.startdate.data,enddate=form.enddate.data,teamcosts=teamcosts)
    return render_template('costcheck.html',title='Cost Accrued check',form=form)