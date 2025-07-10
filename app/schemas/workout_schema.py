from marshmallow import fields
from app import ma
from app.models.workout import Workout

class WorkoutSchema(ma.SQLAlchemyAutoSchema):
    """Schema for serializing workout data."""
    
    class Meta:
        model = Workout
        include_relationships = True  # Include relationships like exercises
        load_instance = True  # Return model instances when deserializing

    # Include any additional fields not automatically captured
    exercises = fields.List(fields.Nested("ExerciseSchema", exclude=("workout",)))
    
    # You can add computed fields if needed
    # example_computed_field = fields.Method("get_example_field")
    
    # def get_example_field(self, obj):
    #     return some_calculation(obj)

# Create schema instances
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
