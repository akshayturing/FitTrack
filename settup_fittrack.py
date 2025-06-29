#!/usr/bin/env python3
"""
setup_fittrack.py - Script to set up the FitTrack application structure
This script creates the necessary directory structure and starter files for the FitTrack app.
"""

import os
import sys

def create_directory(path):
    """Create a directory if it doesn't exist."""
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")
    else:
        print(f"Directory already exists: {path}")

def create_file(path, content=""):
    """Create a file with the given content if it doesn't exist."""
    if not os.path.exists(path):
        with open(path, 'w') as file:
            file.write(content)
        print(f"Created file: {path}")
    else:
        print(f"File already exists: {path}")

def setup_fittrack_app():
    """Set up the FitTrack app directory structure."""
    print("\nSetting up FitTrack application structure...\n")
    
    # Create main directories
    create_directory("app")
    create_directory("app/models")
    create_directory("app/routes")
    create_directory("app/services")
    
    # Create __init__.py files to make directories proper Python packages
    create_file("app/__init__.py", """# app/__init__.py
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    from flask_migrate import Migrate
    from config import config

    # Initialize extensions
    db = SQLAlchemy()
    migrate = Migrate()

    def create_app(config_name='default'):
        \"\"\"Application factory function\"\"\"
        app = Flask(__name__)
        app.config.from_object(config[config_name])
        
        # Initialize extensions with app
        db.init_app(app)
        migrate.init_app(app, db)
        
        # Register blueprints
        from app.routes.user_routes import user_bp
        from app.routes.workout_routes import workout_bp
        
        app.register_blueprint(user_bp, url_prefix='/api/users')
        app.register_blueprint(workout_bp, url_prefix='/api/workouts')
        
        return app
    """)
    create_file("app/models/__init__.py", "# Import models to make them available\nfrom app.models.user import User\nfrom app.models.workout import Workout\n")
    create_file("app/routes/__init__.py", "# Routes package initialization\n")
    create_file("app/services/__init__.py", "# Services package initialization\n")
    
    # Create template files for models
    user_model_content = """# app/models/user.py
    from app import db
    from datetime import datetime
    from werkzeug.security import generate_password_hash, check_password_hash

    class User(db.Model):
        __tablename__ = 'users'
        
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(64), unique=True, nullable=False, index=True)
        email = db.Column(db.String(120), unique=True, nullable=False, index=True)
        _password_hash = db.Column(db.String(128), nullable=False)
        created_at = db.Column(db.DateTime, default=datetime.utcnow)
        
        # Relationships
        workouts = db.relationship('Workout', backref='user', lazy='dynamic', cascade='all, delete-orphan')
        
        @property
        def password(self):
            raise AttributeError('password is not a readable attribute')
            
        @password.setter
        def password(self, password):
            self._password_hash = generate_password_hash(password)
            
        def verify_password(self, password):
            return check_password_hash(self._password_hash, password)
        
        def to_dict(self):
            return {
                'id': self.id,
                'username': self.username,
                'email': self.email,
                'created_at': self.created_at.isoformat() if self.created_at else None
            }
        
        def __repr__(self):
            return f"<User {self.username}>"
    """
    create_file("app/models/user.py", user_model_content)
    
    workout_model_content = """# app/models/workout.py
    from app import db
    from datetime import datetime

    class Workout(db.Model):
        __tablename__ = 'workouts'
        
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
        workout_type = db.Column(db.String(64), nullable=False)
        duration = db.Column(db.Float, nullable=False)  # in minutes
        calories_burned = db.Column(db.Integer)
        distance = db.Column(db.Float)  # in kilometers
        date = db.Column(db.DateTime, default=datetime.utcnow)
        notes = db.Column(db.Text)
        
        def to_dict(self):
            return {
                'id': self.id,
                'user_id': self.user_id,
                'workout_type': self.workout_type,
                'duration': self.duration,
                'calories_burned': self.calories_burned,
                'distance': self.distance,
                'date': self.date.isoformat() if self.date else None,
                'notes': self.notes
            }
        
        def __repr__(self):
            return f"<Workout {self.workout_type} - {self.date}>"
    """
    create_file("app/models/workout.py", workout_model_content)
    
    # Create template files for routes
    user_routes_content = """# app/routes/user_routes.py
    from flask import Blueprint, request, jsonify
    from app.services.user_service import UserService
    from app import db

    user_bp = Blueprint('users', __name__)
    user_service = UserService()

    @user_bp.route('', methods=['POST'])
    def create_user():
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid request data'}), 400
        
        try:
            user = user_service.create_user(data)
            return jsonify(user.to_dict()), 201
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': 'Failed to create user'}), 500

    @user_bp.route('/<int:user_id>', methods=['GET'])
    def get_user(user_id):
        user = user_service.get_user_by_id(user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify(user.to_dict()), 200

    @user_bp.route('/<int:user_id>', methods=['PUT'])
    def update_user(user_id):
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid request data'}), 400
        
        user = user_service.update_user(user_id, data)
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        return jsonify(user.to_dict()), 200

    @user_bp.route('/<int:user_id>', methods=['DELETE'])
    def delete_user(user_id):
        if user_service.delete_user(user_id):
            return jsonify({'message': 'User deleted successfully'}), 200
        return jsonify({'error': 'User not found'}), 404
    """
    create_file("app/routes/user_routes.py", user_routes_content)
    
    workout_routes_content = """# app/routes/workout_routes.py
    from flask import Blueprint, request, jsonify
    from app.services.workout_service import WorkoutService

    workout_bp = Blueprint('workouts', __name__)
    workout_service = WorkoutService()

    @workout_bp.route('', methods=['POST'])
    def create_workout():
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid request data'}), 400
        
        try:
            workout = workout_service.create_workout(data)
            return jsonify(workout.to_dict()), 201
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': 'Failed to create workout'}), 500

    @workout_bp.route('/<int:workout_id>', methods=['GET'])
    def get_workout(workout_id):
        workout = workout_service.get_workout_by_id(workout_id)
        if not workout:
            return jsonify({'error': 'Workout not found'}), 404
        
        return jsonify(workout.to_dict()), 200

    @workout_bp.route('/user/<int:user_id>', methods=['GET'])
    def get_user_workouts(user_id):
        workouts = workout_service.get_workouts_by_user(user_id)
        return jsonify([w.to_dict() for w in workouts]), 200

    @workout_bp.route('/<int:workout_id>', methods=['PUT'])
    def update_workout(workout_id):
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Invalid request data'}), 400
        
        workout = workout_service.update_workout(workout_id, data)
        if not workout:
            return jsonify({'error': 'Workout not found'}), 404
        
        return jsonify(workout.to_dict()), 200

    @workout_bp.route('/<int:workout_id>', methods=['DELETE'])
    def delete_workout(workout_id):
        if workout_service.delete_workout(workout_id):
            return jsonify({'message': 'Workout deleted successfully'}), 200
        return jsonify({'error': 'Workout not found'}), 404
    """
    create_file("app/routes/workout_routes.py", workout_routes_content)
    
    # Create template files for services
    user_service_content = """# app/services/user_service.py
    from app.models.user import User
    from app import db

    class UserService:
        def create_user(self, user_data):
            \"\"\"Create a new user.\"\"\"
            username = user_data.get('username')
            email = user_data.get('email')
            password = user_data.get('password')
            
            if not username or not email or not password:
                raise ValueError('Username, email, and password are required')
            
            # Check if user with this username or email already exists
            if User.query.filter_by(username=username).first():
                raise ValueError(f'Username {username} is already taken')
            
            if User.query.filter_by(email=email).first():
                raise ValueError(f'Email {email} is already registered')
            
            user = User(username=username, email=email)
            user.password = password  # This will trigger the password setter to hash it
            
            db.session.add(user)
            db.session.commit()
            
            return user
        
        def get_user_by_id(self, user_id):
            \"\"\"Get user by ID.\"\"\"
            return User.query.get(user_id)
        
        def update_user(self, user_id, user_data):
            \"\"\"Update user information.\"\"\"
            user = User.query.get(user_id)
            if not user:
                return None
            
            # Update fields
            if 'username' in user_data and user_data['username'] != user.username:
                existing_user = User.query.filter_by(username=user_data['username']).first()
                if existing_user and existing_user.id != user.id:
                    raise ValueError(f'Username {user_data["username"]} is already taken')
                user.username = user_data['username']
                
            if 'email' in user_data and user_data['email'] != user.email:
                existing_user = User.query.filter_by(email=user_data['email']).first()
                if existing_user and existing_user.id != user.id:
                    raise ValueError(f'Email {user_data["email"]} is already registered')
                user.email = user_data['email']
                
            if 'password' in user_data:
                user.password = user_data['password']
            
            db.session.commit()
            return user
        
        def delete_user(self, user_id):
            \"\"\"Delete a user.\"\"\"
            user = User.query.get(user_id)
            if not user:
                return False
            
            db.session.delete(user)
            db.session.commit()
            return True
    """
    create_file("app/services/user_service.py", user_service_content)
    
    workout_service_content = """# app/services/workout_service.py
    from app.models.workout import Workout
    from app.models.user import User
    from app import db

    class WorkoutService:
        def create_workout(self, workout_data):
            \"\"\"Create a new workout.\"\"\"
            required_fields = ['user_id', 'workout_type', 'duration']
            for field in required_fields:
                if field not in workout_data:
                    raise ValueError(f'Missing required field: {field}')
            
            # Verify user exists
            user_id = workout_data.get('user_id')
            user = User.query.get(user_id)
            if not user:
                raise ValueError(f'User with ID {user_id} not found')
            
            workout = Workout(**workout_data)
            db.session.add(workout)
            db.session.commit()
            
            return workout
        
        def get_workout_by_id(self, workout_id):
            \"\"\"Get workout by ID.\"\"\"
            return Workout.query.get(workout_id)
        
        def get_workouts_by_user(self, user_id):
            \"\"\"Get all workouts for a specific user.\"\"\"
            return Workout.query.filter_by(user_id=user_id).order_by(Workout.date.desc()).all()
        
        def update_workout(self, workout_id, workout_data):
            \"\"\"Update workout information.\"\"\"
            workout = Workout.query.get(workout_id)
            if not workout:
                return None
            
            # Update fields
            for key, value in workout_data.items():
                if hasattr(workout, key):
                    setattr(workout, key, value)
            
            db.session.commit()
            return workout
        
        def delete_workout(self, workout_id):
            \"\"\"Delete a workout.\"\"\"
            workout = Workout.query.get(workout_id)
            if not workout:
                return False
            
            db.session.delete(workout)
            db.session.commit()
            return True
    """
    create_file("app/services/workout_service.py", workout_service_content)
    
    # Create config.py
    config_content = """# config.py
    import os
    from datetime import timedelta

    class Config:
        \"\"\"Base configuration.\"\"\"
        SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-please-change-in-production')
        SQLALCHEMY_TRACK_MODIFICATIONS = False
        
        @staticmethod
        def init_app(app):
            pass

    class DevelopmentConfig(Config):
        \"\"\"Development configuration.\"\"\"
        DEBUG = True
        SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL', 'sqlite:///fittrack-dev.db')

    class TestingConfig(Config):
        \"\"\"Testing configuration.\"\"\"
        TESTING = True
        SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL', 'sqlite:///:memory:')
        
    class ProductionConfig(Config):
        \"\"\"Production configuration.\"\"\"
        SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///fittrack.db')

    config = {
        'development': DevelopmentConfig,
        'testing': TestingConfig,
        'production': ProductionConfig,
        'default': DevelopmentConfig
    }
    """
    create_file("config.py", config_content)
    
    # Create run.py
    run_content = """# run.py
    import os
    from app import create_app, db
    from app.models import User, Workout

    app = create_app(os.getenv('FLASK_CONFIG', 'default'))

    @app.cli.command('init_db')
    def init_db():
        \"\"\"Initialize the database.\"\"\"
        db.create_all()
        print('Database initialized.')

    @app.shell_context_processor
    def make_shell_context():
        \"\"\"Configure flask shell command to automatically import app objects.\"\"\"
        return dict(app=app, db=db, User=User, Workout=Workout)

    if __name__ == '__main__':
        app.run(host='0.0.0.0')
    """
    create_file("run.py", run_content)
    
    # Create requirements.txt
    requirements_content = """# Requirements for FitTrack app
    Flask==2.2.3
    Flask-SQLAlchemy==3.0.3
    Flask-Migrate==4.0.4
    Flask-RESTful==0.3.9
    pytest==7.3.1
    python-dotenv==1.0.0
    Werkzeug==2.2.3
    """
    create_file("requirements.txt", requirements_content)
    
    # Create README.md
    readme_content = """# FitTrack App

    A fitness tracking application with a RESTful API that allows users to log and monitor their workouts.

    ## Project Structure"""

setup_fittrack_app()