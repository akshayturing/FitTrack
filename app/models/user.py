# # app/models/user.py
# from app import db
# from datetime import datetime
# from werkzeug.security import generate_password_hash, check_password_hash
# import uuid

# class User(db.Model):
#     __tablename__ = 'users'
    
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     username = db.Column(db.String(64), unique=True, nullable=False, index=True)
#     email = db.Column(db.String(120), unique=True, nullable=False, index=True)
#     _password_hash = db.Column(db.String(128), nullable=False)
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
#     last_login = db.Column(db.DateTime, nullable=True)
#     profile_image = db.Column(db.String(255), nullable=True)
    
#     # Relationships
#     workouts = db.relationship('Workout', backref='user', lazy='dynamic', cascade='all, delete-orphan')
#     assignments = db.relationship('Assignment', backref='user', lazy='dynamic', cascade='all, delete-orphan')
#     sessions = db.relationship('Session', backref='user', lazy='dynamic', cascade='all, delete-orphan')
#     nutrition_goals = db.relationship('NutritionGoal', backref='user', lazy='dynamic', cascade='all, delete-orphan')
#     workouts_created = db.relationship('Workout', backref='creator', foreign_keys='Workout.created_by', lazy='dynamic')
#     workout_assignments = db.relationship('WorkoutAssignment', foreign_keys='WorkoutAssignment.user_id', backref='assignee', lazy='dynamic')
#     workout_sessions = db.relationship('WorkoutSession', backref='user', lazy='dynamic')
    
#     @property
#     def password(self):
#         """Prevent password from being accessed."""
#         raise AttributeError('password is not a readable attribute')
        
#     @password.setter
#     def password(self, password):
#         """Set password to a hashed password."""
#         self._password_hash = generate_password_hash(password)
        
#     def verify_password(self, password):
#         """Check if password matches the hashed password."""
#         return check_password_hash(self._password_hash, password)
    
#     def to_dict(self):
#         """Convert user object to dictionary."""
#         return {
#             'id': self.id,
#             'name': self.name,
#             'username': self.username,
#             'email': self.email,
#             'created_at': self.created_at.isoformat() if self.created_at else None,
#             'last_login': self.last_login.isoformat() if self.last_login else None,
#             'profile_image': self.profile_image,
#             # We don't include relationships by default for security and performance
#         }
    
#     def __repr__(self):
#         """Provide a helpful representation of the user object."""
#         return f"<User {self.username}: {self.name}>"

# app/models/user.py
from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import datetime, timezone

class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, default="User")
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    _password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    last_login = db.Column(db.DateTime, nullable=True)
    profile_image = db.Column(db.String(255), nullable=True)
    
    # Nutrition fields
    calorie_goal = db.Column(db.Integer, nullable=True)
    protein_goal = db.Column(db.Integer, nullable=True)  # in grams
    carbs_goal = db.Column(db.Integer, nullable=True)    # in grams
    fat_goal = db.Column(db.Integer, nullable=True)      # in grams
    water_goal = db.Column(db.Integer, nullable=True)    # in mL
    weight = db.Column(db.Float, nullable=True)          # in kg
    height = db.Column(db.Float, nullable=True)          # in cm
    
    # Relationships
    # workouts_created = db.relationship('Workout', backref='creator', foreign_keys='Workout.created_by', lazy='dynamic')
    #workout_assignments = db.relationship('WorkoutAssignment', foreign_keys='WorkoutAssignment.user_id', backref='assignee', lazy='dynamic')
    assigned_workouts = db.relationship('WorkoutAssignment', foreign_keys='WorkoutAssignment.assigned_by', back_populates='assigner')
    # assigned_to_me = db.relationship('WorkoutAssignment', foreign_keys='WorkoutAssignment.user_id', back_populates='user')
    #assignments = db.relationship('WorkoutAssignment', backref='assigned_user', lazy='dynamic', cascade='all, delete-orphan')
    assignments = db.relationship(
        'WorkoutAssignment',
        foreign_keys='WorkoutAssignment.user_id',
        backref='assigned_user',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    workout_sessions = db.relationship('WorkoutSession', backref='user', lazy='dynamic')
    nutrition_logs = db.relationship('NutritionLog', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    nutrition_profile = db.relationship('NutritionProfile', backref='user', uselist=False, cascade='all, delete-orphan')
    # workouts = db.relationship("Workout", back_populates="user", cascade="all, delete-orphan")
    # __table_args__ = (
    #     db.Index('idx_user_email_username', 'email', 'username'),  # Composite index for login queries
    # )
    # workouts = db.relationship('Workout', back_populates='user', foreign_keys='Workout.created_by')
    workouts = db.relationship("Workout", back_populates="user", foreign_keys="Workout.user_id")

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
    
    def to_dict(self, include_nutrition=False):
        """Convert user object to dictionary."""
        result = {
            'id': self.id,
            'name': self.name,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'profile_image': self.profile_image
        }
        
        if include_nutrition:
            result.update({
                'calorie_goal': self.calorie_goal,
                'protein_goal': self.protein_goal,
                'carbs_goal': self.carbs_goal,
                'fat_goal': self.fat_goal,
                'water_goal': self.water_goal,
                'weight': self.weight,
                'height': self.height
            })
            
        return result
    
    def __repr__(self):
        """Provide a helpful representation of the user object."""
        return f"<User {self.username}: {self.name}>"
    
    def generate_tokens(self):
        """Generate access and refresh tokens for this user"""
        access_token = create_access_token(identity=str(self.id))
        refresh_token = create_refresh_token(identity=str(self.id))
        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': self.to_dict()
        }

    @classmethod
    def get_user_by_username(cls, username):
        """Get a user by username"""
        return cls.query.filter_by(username=username).first()

    @classmethod
    def get_user_by_email(cls, email):
        """Get a user by email"""
        return cls.query.filter_by(email=email).first()
