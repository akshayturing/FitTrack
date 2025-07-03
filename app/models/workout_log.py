# # app/models/workout_log.py

# from datetime import datetime
# from app import db


# class WorkoutSession(db.Model):
#     """Model representing a single workout session logged by a user."""
#     __tablename__ = 'workout_sessions'
    
#     id = db.Column(db.Integer, primary_key=True)
    
#     # Foreign keys
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
#     workout_assignment_id = db.Column(db.Integer, db.ForeignKey('workout_assignments.id', ondelete='SET NULL'), nullable=True)
    
#     # Session metadata
#     session_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
#     duration_minutes = db.Column(db.Integer, nullable=True)
#     notes = db.Column(db.Text, nullable=True)
#     perceived_exertion = db.Column(db.Integer, nullable=True)  # Scale of 1-10
    
#     # Status tracking
#     completed = db.Column(db.Boolean, default=False, nullable=False)
    
#     # Timestamps
#     created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
#     updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
#     # Relationships
#     user = db.relationship('User', backref=db.backref('workout_sessions', lazy=True, cascade='all, delete-orphan'))
#     workout_assignment = db.relationship('WorkoutAssignment', backref=db.backref('workout_sessions', lazy=True))
#     set_logs = db.relationship('SetLog', backref=db.backref('workout_session', lazy=True), cascade='all, delete-orphan')
    
#     def __repr__(self):
#         """String representation of the WorkoutSession object."""
#         return f"<WorkoutSession {self.id} - User {self.user_id} - Date {self.session_date}>"


# class SetLog(db.Model):
#     """Model representing individual exercise sets within a workout session."""
#     __tablename__ = 'set_logs'
    
#     id = db.Column(db.Integer, primary_key=True)
    
#     # Foreign keys
#     workout_session_id = db.Column(db.Integer, db.ForeignKey('workout_sessions.id', ondelete='CASCADE'), nullable=False)
#     exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id', ondelete='SET NULL'), nullable=True)
    
#     # Set details - all nullable to allow for partial logging
#     set_number = db.Column(db.Integer, nullable=True)  # e.g., 1st set, 2nd set
#     reps = db.Column(db.Integer, nullable=True)
#     weight = db.Column(db.Float, nullable=True)  # in pounds or kg
#     weight_unit = db.Column(db.String(10), default='lbs', nullable=True)
    
#     # For timed exercises (e.g., planks)
#     duration_seconds = db.Column(db.Integer, nullable=True)
    
#     # For distance exercises (e.g., running)
#     distance = db.Column(db.Float, nullable=True)
#     distance_unit = db.Column(db.String(10), default='miles', nullable=True)
    
#     # For tracking difficulty
#     difficulty = db.Column(db.Integer, nullable=True)  # Scale of 1-10
    
#     # Optional user notes for this specific set
#     notes = db.Column(db.String(255), nullable=True)
    
#     # Timestamps
#     created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
#     updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
#     # Relationships
#     exercise = db.relationship('Exercise', backref=db.backref('set_logs', lazy=True))
    
#     def __repr__(self):
#         """String representation of the SetLog object."""
#         exercise_name = self.exercise.name if self.exercise else "Unknown Exercise"
#         return f"<SetLog {self.id} - Exercise: {exercise_name} - Reps: {self.reps or 'N/A'} - Weight: {self.weight or 'N/A'}>"

from datetime import datetime
from app import db


class WorkoutSession(db.Model):
    """Model representing a single workout session logged by a user."""
    __tablename__ = 'workout_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign keys with named constraints
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE', name='fk_workout_session_user'), nullable=False)
    workout_assignment_id = db.Column(db.Integer, db.ForeignKey('workout_assignments.id', ondelete='SET NULL', name='fk_workout_session_assignment'), nullable=True)
    
    # Session metadata
    session_date = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    perceived_exertion = db.Column(db.Integer, nullable=True)  # Scale of 1-10
    
    # Status tracking
    completed = db.Column(db.Boolean, default=False, nullable=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    user = db.relationship('User', backref=db.backref('workout_sessions', lazy=True, cascade='all, delete-orphan'))
    workout_assignment = db.relationship('WorkoutAssignment', backref=db.backref('workout_sessions', lazy=True))
    set_logs = db.relationship('SetLog', backref=db.backref('workout_session', lazy=True), cascade='all, delete-orphan')
    
    def __repr__(self):
        """String representation of the WorkoutSession object."""
        return f"<WorkoutSession {self.id} - User {self.user_id} - Date {self.session_date}>"


class SetLog(db.Model):
    """Model representing individual exercise sets within a workout session."""
    __tablename__ = 'set_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Foreign keys with named constraints
    workout_session_id = db.Column(db.Integer, db.ForeignKey('workout_sessions.id', ondelete='CASCADE', name='fk_set_log_session'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id', ondelete='SET NULL', name='fk_set_log_exercise'), nullable=True)
    
    # Set details - all nullable to allow for partial logging
    set_number = db.Column(db.Integer, nullable=True)  # e.g., 1st set, 2nd set
    reps = db.Column(db.Integer, nullable=True)
    weight = db.Column(db.Float, nullable=True)  # in pounds or kg
    weight_unit = db.Column(db.String(10), default='lbs', nullable=True)
    
    # For timed exercises (e.g., planks)
    duration_seconds = db.Column(db.Integer, nullable=True)
    
    # For distance exercises (e.g., running)
    distance = db.Column(db.Float, nullable=True)
    distance_unit = db.Column(db.String(10), default='miles', nullable=True)
    
    # For tracking difficulty
    difficulty = db.Column(db.Integer, nullable=True)  # Scale of 1-10
    
    # Optional user notes for this specific set
    notes = db.Column(db.String(255), nullable=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    exercise = db.relationship('Exercise', backref=db.backref('set_logs', lazy=True))
    
    def __repr__(self):
        """String representation of the SetLog object."""
        exercise_name = self.exercise.name if self.exercise else "Unknown Exercise"
        return f"<SetLog {self.id} - Exercise: {exercise_name} - Reps: {self.reps or 'N/A'} - Weight: {self.weight or 'N/A'}>"