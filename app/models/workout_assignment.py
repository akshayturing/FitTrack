# # # app/models/workout_assignment.py
# # from app import db
# # from datetime import datetime

# # class WorkoutAssignment(db.Model):
# #     __tablename__ = 'workout_assignments'
    
# #     id = db.Column(db.Integer, primary_key=True)
# #     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
# #     workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
# #     assigned_at = db.Column(db.DateTime, default=datetime.utcnow)
# #     assigned_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # Could be a coach
# #     start_date = db.Column(db.Date, nullable=True)
# #     end_date = db.Column(db.Date, nullable=True)
# #     status = db.Column(db.String(20), default='active')  # active, completed, cancelled
# #     frequency = db.Column(db.String(50), nullable=True)  # e.g., "Mon,Wed,Fri" or "2,4,6"
# #     priority = db.Column(db.Integer, default=1)  # Higher number = higher priority
# #     notes = db.Column(db.Text, nullable=True)
    
# #     __table_args__ = (
# #         db.UniqueConstraint('user_id', 'workout_id', name='uix_user_workout'),
# #     )
    
# #     # Relationship with the assigner (optional coach)
# #     assigner = db.relationship('User', foreign_keys=[assigned_by], backref='assigned_workouts')
    
# #     # Relationship with the assignee
# #     user = db.relationship('User', foreign_keys=[user_id], backref='assigned_to_me')
    
# #     def to_dict(self, include_workout=False):
# #         result = {
# #             'id': self.id,
# #             'user_id': self.user_id,
# #             'workout_id': self.workout_id,
# #             'assigned_at': self.assigned_at.isoformat() if self.assigned_at else None,
# #             'assigned_by': self.assigned_by,
# #             'start_date': self.start_date.isoformat() if self.start_date else None,
# #             'end_date': self.end_date.isoformat() if self.end_date else None,
# #             'status': self.status,
# #             'frequency': self.frequency,
# #             'priority': self.priority,
# #             'notes': self.notes
# #         }
        
# #         if include_workout and hasattr(self, 'workout'):
# #             result['workout'] = self.workout.to_dict()
            
# #         return result
    
# #     def __repr__(self):
# #         return f"<WorkoutAssignment {self.id}: {self.workout_id} to {self.user_id}>"
# # app/models/workout_assignment.py
# from app import db
# from datetime import datetime

# class WorkoutAssignment(db.Model):
#     __tablename__ = 'workout_assignments'
    
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
#     workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id', ondelete='CASCADE'), nullable=False, index=True)
#     assigned_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
#     assigned_by = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'), nullable=True, index=True)
#     start_date = db.Column(db.Date, nullable=True)
#     end_date = db.Column(db.Date, nullable=True)
#     status = db.Column(db.String(20), nullable=False, default='active', index=True)  # active, completed, cancelled
#     frequency = db.Column(db.String(50), nullable=True)  # e.g., "Mon,Wed,Fri" or "2,4,6"
#     priority = db.Column(db.Integer, default=1)  # Higher number = higher priority
#     notes = db.Column(db.Text, nullable=True)
    
#     __table_args__ = (
#         # Enforce uniqueness for user and workout combination
#         db.UniqueConstraint('user_id', 'workout_id', name='uix_user_workout_assignment'),
#         # Composite index for frequent status checks
#         db.Index('idx_assignment_user_status', 'user_id', 'status'),
#         # Index for finding assignments within date ranges
#         db.Index('idx_assignment_dates', 'start_date', 'end_date'),
#     )
    
#     # # Relationship with the assigner (optional coach)
#     # assigner = db.relationship('User', foreign_keys=[assigned_by], backref='assigned_workouts')
    
#     # # Relationship with the assignee
#     # user = db.relationship('User', foreign_keys=[user_id], backref='assigned_to_me')
    
#     assigner = db.relationship('User', foreign_keys=[assigned_by], back_populates='assigned_workouts')
#     user = db.relationship('User', foreign_keys=[user_id], back_populates='assigned_to_me')
#     def to_dict(self, include_workout=False):
#         result = {
#             'id': self.id,
#             'user_id': self.user_id,
#             'workout_id': self.workout_id,
#             'assigned_at': self.assigned_at.isoformat() if self.assigned_at else None,
#             'assigned_by': self.assigned_by,
#             'start_date': self.start_date.isoformat() if self.start_date else None,
#             'end_date': self.end_date.isoformat() if self.end_date else None,
#             'status': self.status,
#             'frequency': self.frequency,
#             'priority': self.priority,
#             'notes': self.notes
#         }
        
#         if include_workout and hasattr(self, 'workout'):
#             result['workout'] = self.workout.to_dict()
            
#         return result
    
#     def __repr__(self):
#         return f"<WorkoutAssignment {self.id}: {self.workout_id} to {self.user_id}>"

# app/models/workout.py
from app import db
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship

class Workout(db.Model):
    """
    Workout model to represent a collection of exercises.
    
    Attributes:
        id (int): Primary key
        name (str): Name of the workout
        description (str): Detailed description of the workout
        created_at (datetime): When the workout was created
        user_id (int): Foreign key to user who created the workout
        exercises (relationship): Relationship to exercises through WorkoutExercise
    """
    __tablename__ = 'workouts'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    # Relationship to user
    user = relationship("User", back_populates="workouts")
    
    # Relationship to workout exercises
    workout_exercises = relationship("WorkoutExercise", back_populates="workout", 
                                    cascade="all, delete-orphan", order_by="WorkoutExercise.position")
    
    # Convenience property to access exercises directly
    @property
    def exercises(self):
        return [we.exercise for we in self.workout_exercises]
    
    def __repr__(self):
        """String representation of the Workout object."""
        return f"<Workout {self.name} (id: {self.id})>"
