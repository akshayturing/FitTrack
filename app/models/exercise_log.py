# app/models/exercise_log.py
from app import db
from datetime import datetime

class ExerciseLog(db.Model):
    __tablename__ = 'exercise_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('sessions.id'), nullable=False)
    exercise_name = db.Column(db.String(100), nullable=False)
    sets = db.Column(db.Integer, nullable=True)
    reps = db.Column(db.Integer, nullable=True)
    weight = db.Column(db.Float, nullable=True)  # in kg
    duration = db.Column(db.Integer, nullable=True)  # in seconds
    distance = db.Column(db.Float, nullable=True)  # in km
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text, nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'session_id': self.session_id,
            'exercise_name': self.exercise_name,
            'sets': self.sets,
            'reps': self.reps,
            'weight': self.weight,
            'duration': self.duration,
            'distance': self.distance,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'notes': self.notes
        }
    
    def __repr__(self):
        return f"<ExerciseLog {self.exercise_name} for Session {self.session_id}>"