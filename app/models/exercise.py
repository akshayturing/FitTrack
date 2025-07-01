# # app/models/exercise.py
# from app import db
# from datetime import datetime

# class Exercise(db.Model):
#     __tablename__ = 'exercises'
    
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False, unique=True)
#     description = db.Column(db.Text, nullable=True)
#     muscle_group = db.Column(db.String(50), nullable=True)
#     secondary_muscle_groups = db.Column(db.String(100), nullable=True)
#     difficulty = db.Column(db.String(20), nullable=True)  # beginner, intermediate, advanced
#     equipment = db.Column(db.String(100), nullable=True)
#     default_sets = db.Column(db.Integer, nullable=True)
#     default_reps = db.Column(db.Integer, nullable=True)
#     instructions = db.Column(db.Text, nullable=True)
#     demo_url = db.Column(db.String(255), nullable=True)  # video demonstration URL
#     created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
#     # Relationships - connects to workouts via WorkoutExercise join table
#     workouts = db.relationship('WorkoutExercise', backref='exercise', lazy='dynamic')
#     set_logs = db.relationship('SetLog', backref='exercise', lazy='dynamic')
    
#     def to_dict(self):
#         return {
#             'id': self.id,
#             'name': self.name,
#             'description': self.description,
#             'muscle_group': self.muscle_group,
#             'secondary_muscle_groups': self.secondary_muscle_groups,
#             'difficulty': self.difficulty,
#             'equipment': self.equipment,
#             'default_sets': self.default_sets,
#             'default_reps': self.default_reps,
#             'instructions': self.instructions,
#             'demo_url': self.demo_url,
#             'created_at': self.created_at.isoformat() if self.created_at else None
#         }
    
#     def __repr__(self):
#         return f"<Exercise {self.id}: {self.name}>"
# app/models/exercise.py
from app import db
from sqlalchemy import Column, Integer, String, Text, Enum
import enum

class ExerciseType(enum.Enum):
    STRENGTH = "strength"
    CARDIO = "cardio"
    FLEXIBILITY = "flexibility"
    BALANCE = "balance"
    
class Exercise(db.Model):
    """
    Exercise model to represent reusable movement templates.
    
    Attributes:
        id (int): Primary key
        name (str): Name of the exercise
        type (ExerciseType): Type of exercise (strength, cardio, etc.)
        description (str): Detailed description of the exercise
        default_reps (int): Default number of repetitions recommended
        default_sets (int): Default number of sets recommended
        target_muscles (str): Comma-separated list of targeted muscle groups
        instructions (str): Step-by-step instructions for performing the exercise
    """
    __tablename__ = 'exercises'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    type = Column(Enum(ExerciseType), nullable=False)
    description = Column(Text, nullable=True)
    default_reps = Column(Integer, nullable=True)
    default_sets = Column(Integer, nullable=True)
    target_muscles = Column(String(200), nullable=True)
    instructions = Column(Text, nullable=True)
    
    def __repr__(self):
        """String representation of the Exercise object."""
        return f"<Exercise {self.name} ({self.type.value})>"