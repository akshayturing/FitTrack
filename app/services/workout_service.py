# app/services/workout_service.py
from app.models.workout import Workout
from app.models.user import User
from app import db
from app.models.workout_assignment import WorkoutAssignment
import app
from sqlalchemy.exc import SQLAlchemyError
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

    # Add this method to your existing WorkoutService class
    def get_public_workouts(self, filters=None):
        """
        Get all public workouts with optional filtering.
        
        Args:
            filters (dict, optional): Dictionary containing filter parameters.
                Possible filters:
                - category: Filter by workout category
                - difficulty_level: Filter by difficulty level
                - duration: Filter by max duration in minutes
                - search: Search in title and description
                
        Returns:
            list: List of Workout objects matching the criteria
        """
        # Start with base query for public workouts
        query = Workout.query.filter_by(is_public=True)
        
        # Apply filters if provided
        if filters:
            # Filter by category
            if 'category' in filters and filters['category']:
                query = query.filter(Workout.category == filters['category'])
            
            # Filter by difficulty level
            if 'difficulty_level' in filters and filters['difficulty_level']:
                query = query.filter(Workout.difficulty_level == filters['difficulty_level'])
            
            # Filter by duration (max duration)
            if 'duration' in filters and filters['duration']:
                try:
                    max_duration = float(filters['duration'])
                    query = query.filter(Workout.duration <= max_duration)
                except (ValueError, TypeError):
                    # If duration is not a valid number, ignore this filter
                    pass
                    
            # Search in title and description
            if 'search' in filters and filters['search']:
                search_term = f"%{filters['search']}%"
                query = query.filter(
                    db.or_(
                        Workout.title.ilike(search_term),
                        Workout.description.ilike(search_term)
                    )
                )
        
        # Order by newest first
        query = query.order_by(Workout.date.desc())
        
        return query.all()
    
    @staticmethod
    def get_user_assigned_workouts(user_id):
        """
        Get all workouts assigned to a specific user
        
        Args:
            user_id (int): ID of the user
        
        Returns:
            list: List of Workout objects
            
        Raises:
            SQLAlchemyError: If database error occurs
        """
        try:
            # Get all workout assignments for the user
            assignments = WorkoutAssignment.query.filter_by(
                user_id=user_id, 
                is_active=True
            ).all()
            
            # Extract workout IDs from assignments
            workout_ids = [assignment.workout_id for assignment in assignments]
            
            if not workout_ids:
                return []
                
            # Get all relevant workouts
            return Workout.query.filter(Workout.id.in_(workout_ids)).all()
        except SQLAlchemyError as e:
            raise
    
    @staticmethod
    def is_workout_assigned_to_user(user_id, workout_id):
        """
        Check if a workout is assigned to a user
        
        Args:
            user_id (int): ID of the user
            workout_id (int): ID of the workout
            
        Returns:
            bool: True if workout is assigned to user, False otherwise
        """
        assignment = WorkoutAssignment.query.filter_by(
            user_id=user_id,
            workout_id=workout_id,
            is_active=True
        ).first()
        
        return assignment is not None
