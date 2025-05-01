import os
basedir = os.path.abspath(os.path.dirname(__file__))
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://postgres:admin@localhost:5432/booking'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OAUTH_CLIENT_ID = os.environ.get('OAUTH_CLIENT_ID') or 'your-client-id'
    OAUTH_CLIENT_SECRET = os.environ.get('OAUTH_CLIENT_SECRET') or 'your-client-secret'
    OAUTH_REDIRECT_URI = os.environ.get('OAUTH_REDIRECT_URI') or 'http://localhost:5000/oauth/callback'