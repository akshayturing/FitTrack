# app/models/exercise.py
from app import db
from datetime import datetime

class Exercise(db.Model):
    __tablename__ = 'exercises'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    muscle_group = db.Column(db.String(50), nullable=True)
    secondary_muscle_groups = db.Column(db.String(100), nullable=True)
    difficulty = db.Column(db.String(20), nullable=True)  # beginner, intermediate, advanced
    equipment = db.Column(db.String(100), nullable=True)
    default_sets = db.Column(db.Integer, nullable=True)
    default_reps = db.Column(db.Integer, nullable=True)
    instructions = db.Column(db.Text, nullable=True)
    demo_url = db.Column(db.String(255), nullable=True)  # video demonstration URL
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships - connects to workouts via WorkoutExercise join table
    workouts = db.relationship('WorkoutExercise', backref='exercise', lazy='dynamic')
    set_logs = db.relationship('SetLog', backref='exercise', lazy='dynamic')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'muscle_group': self.muscle_group,
            'secondary_muscle_groups': self.secondary_muscle_groups,
            'difficulty': self.difficulty,
            'equipment': self.equipment,
            'default_sets': self.default_sets,
            'default_reps': self.default_reps,
            'instructions': self.instructions,
            'demo_url': self.demo_url,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f"<Exercise {self.id}: {self.name}>"