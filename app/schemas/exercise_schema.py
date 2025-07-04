from app import ma
from app.models.exercise import Exercise

class ExerciseSchema(ma.SQLAlchemyAutoSchema):
    """Schema for serializing exercise data."""
    
    class Meta:
        model = Exercise
        include_fk = True

# Create schema instances
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
