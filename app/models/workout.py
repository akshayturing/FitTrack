# # app/models/workout.py
# from app import db
# from datetime import datetime

# class Workout(db.Model):
#     __tablename__ = 'workouts'
    
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     workout_type = db.Column(db.String(64), nullable=False)
#     duration = db.Column(db.Float, nullable=False)  # in minutes
#     calories_burned = db.Column(db.Integer)
#     distance = db.Column(db.Float)  # in kilometers
#     date = db.Column(db.DateTime, default=datetime.utcnow)
#     notes = db.Column(db.Text)
    
#     def to_dict(self):
#         return {
#             'id': self.id,
#             'user_id': self.user_id,
#             'workout_type': self.workout_type,
#             'duration': self.duration,
#             'calories_burned': self.calories_burned,
#             'distance': self.distance,
#             'date': self.date.isoformat() if self.date else None,
#             'notes': self.notes
#         }
    
#     def __repr__(self):
#         return f"<Workout {self.workout_type} - {self.date}>"
# app/models/workout.py
from app import db
from datetime import datetime

class Workout(db.Model):
    __tablename__ = 'workouts'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=True)
    workout_type = db.Column(db.String(50), nullable=True)
    description = db.Column(db.Text, nullable=True)
    difficulty_level = db.Column(db.String(20), nullable=True)  # beginner, intermediate, advanced
    estimated_duration = db.Column(db.Integer, nullable=True)  # in minutes
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    is_public = db.Column(db.Boolean, default=True)
    image_url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    # assignments = db.relationship('WorkoutAssignment', backref='assigned_workout', lazy='dynamic', cascade='all, delete-orphan')
    
    # Relationships
    # exercises = db.relationship('WorkoutExercise', backref='workout', lazy='dynamic', cascade='all, delete-orphan')
    # assignments = db.relationship('WorkoutAssignment', backref='workout', lazy='dynamic', cascade='all, delete-orphan')
    # sessions = db.relationship('WorkoutSession', backref='workout', lazy='dynamic')
    # Inside Workout
    # user = db.relationship("User", back_populates="workouts")
    # user = db.relationship('User', back_populates='workouts', foreign_keys=[created_by])
    user = db.relationship("User", back_populates="workouts", foreign_keys=[user_id])
    assignments = db.relationship(
        'WorkoutAssignment',
        foreign_keys='WorkoutAssignment.workout_id',
        backref='assigned_workout',
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates="workout",
        cascade="all, delete-orphan",
        order_by="WorkoutExercise.position"
    )
    # created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    def to_dict(self, include_exercises=False):
        result = {
            'id': self.id,
            'title': self.title,
            'category': self.category,
            'description': self.description,
            'difficulty_level': self.difficulty_level,
            'estimated_duration': self.estimated_duration,
            'created_by': self.created_by,
            'is_public': self.is_public,
            'image_url': self.image_url,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_exercises:
            result['exercises'] = [we.to_dict() for we in self.exercises]
            
        return result
    
    def __repr__(self):
        return f"<Workout {self.id}: {self.title}>"