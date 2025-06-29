# app/services/workout_service.py
from app.models.workout import Workout
from app.models.user import User
from app import db

class WorkoutService:
    def create_workout(self, workout_data):
        """Create a new workout."""
        required_fields = ['user_id', 'workout_type', 'duration']
        for field in required_fields:
            if field not in workout_data:
                raise ValueError(f'Missing required field: {field}')
        
        # Verify user exists
        user_id = workout_data.get('user_id')
        user = User.query.get(user_id)
        if not user:
            raise ValueError(f'User with ID {user_id} not found')
        
        workout = Workout(**workout_data)
        db.session.add(workout)
        db.session.commit()
        
        return workout
    
    def get_workout_by_id(self, workout_id):
        """Get workout by ID."""
        return Workout.query.get(workout_id)
    
    def get_workouts_by_user(self, user_id):
        """Get all workouts for a specific user."""
        return Workout.query.filter_by(user_id=user_id).order_by(Workout.date.desc()).all()
    
    def update_workout(self, workout_id, workout_data):
        """Update workout information."""
        workout = Workout.query.get(workout_id)
        if not workout:
            return None
        
        # Update fields
        for key, value in workout_data.items():
            if hasattr(workout, key):
                setattr(workout, key, value)
        
        db.session.commit()
        return workout
    
    def delete_workout(self, workout_id):
        """Delete a workout."""
        workout = Workout.query.get(workout_id)
        if not workout:
            return False
        
        db.session.delete(workout)
        db.session.commit()
        return True
