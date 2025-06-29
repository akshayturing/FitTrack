# app/models/workout.py
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
