# from app import db
# from datetime import datetime

# class SetLog(db.Model):
#     __tablename__ = 'set_logs'
    
#     id = db.Column(db.Integer, primary_key=True)
#     session_id = db.Column(db.Integer, db.ForeignKey('workout_sessions.id'), nullable=False)
#     exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
#     set_number = db.Column(db.Integer, nullable=False)
#     reps = db.Column(db.Integer, nullable=True)
#     weight = db.Column(db.Float, nullable=True)  # in kg
#     time_duration = db.Column(db.Integer, nullable=True)  # in seconds, for timed exercises
#     distance = db.Column(db.Float, nullable=True)  # for distance-based exercises
#     rpe = db.Column(db.Float, nullable=True)  # Rate of Perceived Exertion (1-10)
#     completed = db.Column(db.Boolean, default=True)
#     notes = db.Column(db.Text, nullable=True)
#     logged_at = db.Column(db.DateTime, default=datetime.utcnow)
    
#     __table_args__ = (
#         db.UniqueConstraint('session_id', 'exercise_id', 'set_number', name='uix_session_exercise_set'),
#     )
    
#     def to_dict(self):
#         return {
#             'id': self.id,
#             'session_id': self.session_id,
#             'exercise_id': self.exercise_id,
#             'set_number': self.set_number,
#             'reps': self.reps,
#             'weight': self.weight,
#             'time_duration': self.time_duration,
#             'distance': self.distance,
#             'rpe': self.rpe,
#             'completed': self.completed,
#             'notes': self.notes,
#             'logged_at': self.logged_at.isoformat() if self.logged_at else None
#         }
    
#     def __repr__(self):
#         return f"<SetLog {self.id}: Session {self.session_id} - Exercise {self.exercise_id} - Set {self.set_number}>"
# app/models/set_log.py
from app import db
from datetime import datetime

class SetLog(db.Model):
    __tablename__ = 'set_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('workout_sessions.id', ondelete='CASCADE'), nullable=False, index=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id', ondelete='CASCADE'), nullable=False, index=True)
    set_number = db.Column(db.Integer, nullable=False)
    reps = db.Column(db.Integer, nullable=True)
    weight = db.Column(db.Float, nullable=True)  # in kg
    time_duration = db.Column(db.Integer, nullable=True)  # in seconds, for timed exercises
    distance = db.Column(db.Float, nullable=True)  # for distance-based exercises
    rpe = db.Column(db.Float, nullable=True)  # Rate of Perceived Exertion (1-10)
    completed = db.Column(db.Boolean, default=True, nullable=False)
    notes = db.Column(db.Text, nullable=True)
    logged_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    __table_args__ = (
        # Enforce uniqueness for session, exercise, and set_number combination
        db.UniqueConstraint('session_id', 'exercise_id', 'set_number', name='uix_session_exercise_set'),
        # Index for performance tracking queries
        db.Index('idx_set_exercise_date', 'exercise_id', 'logged_at'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'session_id': self.session_id,
            'exercise_id': self.exercise_id,
            'set_number': self.set_number,
            'reps': self.reps,
            'weight': self.weight,
            'time_duration': self.time_duration,
            'distance': self.distance,
            'rpe': self.rpe,
            'completed': self.completed,
            'notes': self.notes,
            'logged_at': self.logged_at.isoformat() if self.logged_at else None
        }
    
    def __repr__(self):
        return f"<SetLog {self.id}: Session {self.session_id} - Exercise {self.exercise_id} - Set {self.set_number}>"