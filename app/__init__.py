# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name='default'):
    """Application factory function"""
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
