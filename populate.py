import os
from datetime import datetime
from app import app, db
from app.models import Room, User, Team, Meeting

def populate():
    with app.app_context():  # Ensure operations are within an app context

        # Drop all tables and recreate them
        db.drop_all()
        db.create_all()

        # Create dummy teams if they don't already exist
        team_names = ["Admin", "Devops", "HR", "Visitor"]
        teams = []
        for name in team_names:
            team = Team.query.filter_by(teamName=name).first()
            if not team:
                team = Team(teamName=name)
                db.session.add(team)
            teams.append(team)
        db.session.commit()

        # Create dummy users if they don't already exist
        user_data = [
            {"username": "admin_user", "team": "Admin"},
            {"username": "devops_user", "team": "Devops"},
            {"username": "hr_user", "team": "HR"},
            {"username": "visitor_user", "team": "Visitor"},
        ]
        for data in user_data:
            user = User.query.filter_by(username=data["username"]).first()
            if not user:
                user = User(username=data["username"], team=data["team"])
                user.set_password(data["username"])  # Set password as username for simplicity
                db.session.add(user)
        db.session.commit()

        # Create dummy rooms if they don't already exist
        room_data = [
            {"roomName": "Conference Room A", "telephone": True, "projector": True, "whiteboard": True},
            {"roomName": "Conference Room B", "telephone": False, "projector": True, "whiteboard": False},
            {"roomName": "Meeting Room C", "telephone": True, "projector": False, "whiteboard": True},
        ]
        for data in room_data:
            room = Room.query.filter_by(roomName=data["roomName"]).first()
            if not room:
                room = Room(**data)
                db.session.add(room)
        db.session.commit()

        # Create dummy meetings if they don't already exist
        meeting_data = [
            {
                "title": "Admin Meeting",
                "teamId": teams[0].id,
                "roomId": Room.query.filter_by(roomName="Conference Room A").first().id,
                "bookerId": User.query.filter_by(username="admin_user").first().id,
                "date": datetime(2023, 10, 1),
                "startTime": 9,
                "endTime": 11,
            },
            {
                "title": "Devops Standup",
                "teamId": teams[1].id,
                "roomId": Room.query.filter_by(roomName="Conference Room B").first().id,
                "bookerId": User.query.filter_by(username="devops_user").first().id,
                "date": datetime(2023, 10, 2),
                "startTime": 10,
                "endTime": 11,
            },
            {
                "title": "HR Orientation",
                "teamId": teams[2].id,
                "roomId": Room.query.filter_by(roomName="Meeting Room C").first().id,
                "bookerId": User.query.filter_by(username="hr_user").first().id,
                "date": datetime(2023, 10, 3),
                "startTime": 14,
                "endTime": 16,
            },
        ]
        for data in meeting_data:
            meeting = Meeting.query.filter_by(title=data["title"]).first()
            if not meeting:
                meeting = Meeting(**data)
                db.session.add(meeting)
        db.session.commit()

        print("Database reset and dummy data populated successfully!")

if __name__ == '__main__':
    populate()