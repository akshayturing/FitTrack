from app import db
from datetime import datetime

class WorkoutSession(db.Model):
    __tablename__ = 'workout_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    started_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    duration = db.Column(db.Integer, nullable=True)  # in seconds
    calories_burned = db.Column(db.Integer, nullable=True)
    difficulty_rating = db.Column(db.Integer, nullable=True)  # 1-10 user rating
    mood = db.Column(db.String(50), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    
    # Relationships
    set_logs = db.relationship('SetLog', backref='session', lazy='dynamic', cascade='all, delete-orphan')
    
    def calculate_duration(self):
        """Calculate session duration based on start and end times."""
        if not self.completed_at:
            return 0
        delta = self.completed_at - self.started_at
        return int(delta.total_seconds())
    
    def update_duration(self):
        """Update the duration field based on start and end times."""
        if self.completed_at:
            self.duration = self.calculate_duration()
    
    def to_dict(self, include_sets=False):
        result = {
            'id': self.id,
            'user_id': self.user_id,
            'workout_id': self.workout_id,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'duration': self.duration,
            'calories_burned': self.calories_burned,
            'difficulty_rating': self.difficulty_rating,
            'mood': self.mood,
            'notes': self.notes
        }
        
        if include_sets:
            result['set_logs'] = [log.to_dict() for log in self.set_logs]
            
        return result
    
    def __repr__(self):
        return f"<WorkoutSession {self.id}: {self.user_id} - {self.workout_id}>"