# run.py
import os
from app import create_app, db
from app.models import User, Workout

app = create_app(os.getenv('FLASK_CONFIG', 'default'))

@app.cli.command('init_db')
def init_db():
    """Initialize the database."""
    with app.app_context():
        db.create_all()
    print('Database initialized.')

@app.shell_context_processor
def make_shell_context():
    """Configure flask shell command to automatically import app objects."""
    return dict(app=app, db=db, User=User, Workout=Workout)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
