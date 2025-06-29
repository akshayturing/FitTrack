# app/models/user.py
from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
import uuid

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    _password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    profile_image = db.Column(db.String(255), nullable=True)
    
    # Relationships
    workouts = db.relationship('Workout', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    assignments = db.relationship('Assignment', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    sessions = db.relationship('Session', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    nutrition_goals = db.relationship('NutritionGoal', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    @property
    def password(self):
        """Prevent password from being accessed."""
        raise AttributeError('password is not a readable attribute')
        
    @password.setter
    def password(self, password):
        """Set password to a hashed password."""
        self._password_hash = generate_password_hash(password)
        
    def verify_password(self, password):
        """Check if password matches the hashed password."""
        return check_password_hash(self._password_hash, password)
    
    def to_dict(self):
        """Convert user object to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'profile_image': self.profile_image,
            # We don't include relationships by default for security and performance
        }
    
    def __repr__(self):
        """Provide a helpful representation of the user object."""
        return f"<User {self.username}: {self.name}>"
