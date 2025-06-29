# app/models/session.py
from app import db
from datetime import datetime

class Session(db.Model):
    __tablename__ = 'sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    mood = db.Column(db.String(50), nullable=True)
    energy_level = db.Column(db.Integer, nullable=True)  # Scale of 1-10
    
    # Relationship with exercises performed
    exercise_logs = db.relationship('ExerciseLog', backref='session', lazy='dynamic', cascade='all, delete-orphan')
    
    def duration_minutes(self):
        """Calculate session duration in minutes."""
        if not self.end_time:
            return 0
        delta = self.end_time - self.start_time
        return delta.total_seconds() / 60
        
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'notes': self.notes,
            'mood': self.mood,
            'energy_level': self.energy_level,
            'duration_minutes': self.duration_minutes()
        }
    
    def __repr__(self):
        return f"<Session {self.id} for User {self.user_id}>"