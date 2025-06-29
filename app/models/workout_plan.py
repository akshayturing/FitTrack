# app/models/workout_plan.py
from app import db
from datetime import datetime

class WorkoutPlan(db.Model):
    __tablename__ = 'workout_plans'
    
    id = db.Column(db.Integer, primary_key=True)
    assignment_id = db.Column(db.Integer, db.ForeignKey('assignments.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    day_of_week = db.Column(db.Integer, nullable=True)  # 0-6 for Monday-Sunday
    exercises = db.Column(db.Text, nullable=True)  # JSON string of exercises
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'assignment_id': self.assignment_id,
            'title': self.title,
            'description': self.description,
            'day_of_week': self.day_of_week,
            'exercises': self.exercises,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f"<WorkoutPlan {self.title} for Assignment {self.assignment_id}>"