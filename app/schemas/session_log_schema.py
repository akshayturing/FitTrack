from app import ma
from app.models.workout_log import WorkoutSession, SetLog
from app.models.exercise import Exercise
from marshmallow import fields

class ExerciseSchema(ma.SQLAlchemyAutoSchema):
    """Schema for serializing exercises."""
    class Meta:
        model = Exercise
        include_fk = True

class SetLogSchema(ma.SQLAlchemyAutoSchema):
    """Schema for serializing set logs."""
    class Meta:
        model = SetLog
        include_fk = True
        
    # Add exercise details
    exercise = fields.Nested(ExerciseSchema, exclude=('created_at', 'updated_at'))

class WorkoutSessionSchema(ma.SQLAlchemyAutoSchema):
    """Schema for serializing workout sessions."""
    class Meta:
        model = WorkoutSession
        include_fk = True
        
    # Include nested set logs organized by exercise
    set_logs = fields.Nested(SetLogSchema, many=True)
    
    # Dynamically organize sets by exercise
    exercises = fields.Method('get_exercises_with_sets')
    
    def get_exercises_with_sets(self, obj):
        """Organize set logs by exercise for cleaner hierarchical response."""
        exercise_data = {}
        
        # Group sets by exercise
        for set_log in obj.set_logs:
            if set_log.exercise_id not in exercise_data:
                # Include basic exercise info
                if set_log.exercise:
                    exercise_data[set_log.exercise_id] = {
                        'id': set_log.exercise_id,
                        'name': set_log.exercise.name,
                        'type': set_log.exercise.type,
                        'target_muscles': set_log.exercise.target_muscles,
                        'sets': []
                    }
                else:
                    # Handle case where exercise might have been deleted
                    exercise_data[set_log.exercise_id] = {
                        'id': set_log.exercise_id,
                        'name': 'Unknown Exercise',
                        'sets': []
                    }
                
            # Add the set data
            set_data = {
                'id': set_log.id,
                'set_number': set_log.set_number,
                'reps': set_log.reps,
                'weight': set_log.weight,
                'weight_unit': set_log.weight_unit,
                'duration_seconds': set_log.duration_seconds,
                'distance': set_log.distance,
                'distance_unit': set_log.distance_unit,
                'difficulty': set_log.difficulty,
                'notes': set_log.notes
            }
            
            exercise_data[set_log.exercise_id]['sets'].append(set_data)
        
        # Convert to list for proper JSON response
        return list(exercise_data.values())


# Create schema instances
session_log_schema = WorkoutSessionSchema()
session_logs_schema = WorkoutSessionSchema(many=True)
set_log_schema = SetLogSchema()
set_logs_schema = SetLogSchema(many=True)
