# app/models/workout_exercise.py
from app import db

class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'
    
    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    order_index = db.Column(db.Integer, nullable=False)  # Position in workout
    sets = db.Column(db.Integer, nullable=False, default=3)
    reps = db.Column(db.String(50), nullable=False, default='10')  # String to allow for ranges like '8-10'
    rest_seconds = db.Column(db.Integer, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    
    __table_args__ = (
        db.UniqueConstraint('workout_id', 'exercise_id', name='uix_workout_exercise'),
    )
    
    def to_dict(self, include_exercise_details=False):
        result = {
            'id': self.id,
            'workout_id': self.workout_id,
            'exercise_id': self.exercise_id,
            'order_index': self.order_index,
            'sets': self.sets,
            'reps': self.reps,
            'rest_seconds': self.rest_seconds,
            'notes': self.notes
        }
        
        if include_exercise_details and hasattr(self, 'exercise'):
            result['exercise'] = self.exercise.to_dict()
            
        return result
    
    def __repr__(self):
        return f"<WorkoutExercise {self.workout_id}:{self.exercise_id}>"