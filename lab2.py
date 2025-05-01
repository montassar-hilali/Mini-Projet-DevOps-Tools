#from flask import render_template
from app import app, db
from app.models import User,Room


@app.shell_context_processor
def make_shell_context():
    # This decorator registers a shell context processor, which adds objects 
    # to the shell session when using `flask shell`. This makes it easier 
    return {
        'db': db,
        'User': User,
        'Room': Room
    }


if __name__ == '__main__':
    app.debug=True
    app.run(host='127.0.0.1', port=5000)
    