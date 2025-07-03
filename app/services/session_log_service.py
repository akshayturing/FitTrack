from app import db
from app.models.workout_log import WorkoutSession, SetLog
from app.models.exercise import Exercise
from sqlalchemy import and_, or_, desc
from datetime import datetime, timedelta

class SessionLogService:
    """Service for handling workout session logging operations."""
    
    def create_session_log(self, user_id, session_data):
        """
        Create a new workout session log with exercises and sets.
        
        Args:
            user_id (int): ID of the user logging the workout
            session_data (dict): Data for the workout session, including exercises and sets
            
        Returns:
            WorkoutSession: The newly created workout session with all related data
        """
        # Extract session metadata
        workout_assignment_id = session_data.get('workout_assignment_id')
        
        # Parse session date if provided, otherwise use current time
        session_date = datetime.utcnow()
        if session_data.get('session_date'):
            try:
                session_date = datetime.fromisoformat(session_data.get('session_date').replace('Z', '+00:00'))
            except (ValueError, TypeError):
                # Handle various date formats or keep default
                try:
                    session_date = datetime.strptime(session_data.get('session_date'), '%Y-%m-%dT%H:%M:%S')
                except (ValueError, TypeError):
                    pass
        
        # Create workout session
        session = WorkoutSession(
            user_id=user_id,
            workout_assignment_id=workout_assignment_id,
            session_date=session_date,
            duration_minutes=session_data.get('duration_minutes'),
            notes=session_data.get('notes'),
            perceived_exertion=session_data.get('perceived_exertion'),
            completed=session_data.get('completed', False)
        )
        
        db.session.add(session)
        db.session.flush()  # Get the ID without committing
        
        # Process exercise sets if provided
        exercises_data = session_data.get('exercises', [])
        for exercise_data in exercises_data:
            exercise_id = exercise_data.get('exercise_id')
            
            # Verify the exercise exists
            exercise = Exercise.query.get(exercise_id)
            if not exercise:
                db.session.rollback()
                raise ValueError(f"Exercise with ID {exercise_id} does not exist")
            
            # Process sets for this exercise
            sets_data = exercise_data.get('sets', [])
            for i, set_data in enumerate(sets_data, 1):
                # Use provided set number or default to incremental
                set_number = set_data.get('set_number', i)
                
                set_log = SetLog(
                    workout_session_id=session.id,
                    exercise_id=exercise_id,
                    set_number=set_number,
                    reps=set_data.get('reps'),
                    weight=set_data.get('weight'),
                    weight_unit=set_data.get('weight_unit', 'lbs'),
                    duration_seconds=set_data.get('duration_seconds'),
                    distance=set_data.get('distance'),
                    distance_unit=set_data.get('distance_unit', 'miles'),
                    difficulty=set_data.get('difficulty'),
                    notes=set_data.get('notes')
                )
                
                db.session.add(set_log)
        
        # Commit the transaction
        db.session.commit()
        return session
    
    def get_session_logs(self, filters=None, page=1, per_page=10):
        """
        Get workout session logs with optional filtering and pagination.
        
        Args:
            filters (dict): Filtering criteria
            page (int): Page number for pagination
            per_page (int): Items per page
            
        Returns:
            dict: Paginated workout sessions with metadata
        """
        query = WorkoutSession.query
        
        if filters:
            # User filter
            if 'user_id' in filters:
                query = query.filter(WorkoutSession.user_id == filters['user_id'])
            
            # Date range filters
            if 'start_date' in filters:
                query = query.filter(WorkoutSession.session_date >= filters['start_date'])
            if 'end_date' in filters:
                # Add one day to include the end date completely
                end_date = filters['end_date'] + timedelta(days=1)
                query = query.filter(WorkoutSession.session_date < end_date)
            
            # Other filters
            if 'workout_id' in filters:
                # This would require a join with workout_assignments
                # Assuming workout_assignment has a workout_id field
                query = query.filter(WorkoutSession.workout_assignment_id.in_(
                    db.session.query(WorkoutAssignment.id)\
                    .filter_by(workout_id=filters['workout_id'])\
                    .subquery()
                ))
                
            if 'workout_assignment_id' in filters:
                query = query.filter(WorkoutSession.workout_assignment_id == filters['workout_assignment_id'])
                
            if 'completed' in filters:
                query = query.filter(WorkoutSession.completed == filters['completed'])
        
        # Order by most recent first
        query = query.order_by(desc(WorkoutSession.session_date))
        
        # Apply pagination
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return {
            'items': session_logs_schema.dump(pagination.items),
            'page': pagination.page,
            'pages': pagination.pages,
            'total': pagination.total
        }
    
    def get_session_log_by_id(self, session_id):
        """
        Get a specific workout session log by ID.
        
        Args:
            session_id (int): ID of the workout session
            
        Returns:
            WorkoutSession: The requested workout session with all related data
        """
        return WorkoutSession.query.get(session_id)
    
    def update_session_log(self, session_id, session_data):
        """
        Update an existing workout session log.
        
        Args:
            session_id (int): ID of the workout session to update
            session_data (dict): Updated data for the workout session
            
        Returns:
            WorkoutSession: The updated workout session
        """
        session = WorkoutSession.query.get(session_id)
        if not session:
            raise ValueError(f"Workout session with ID {session_id} does not exist")
            
        # Update session metadata
        if 'workout_assignment_id' in session_data:
            session.workout_assignment_id = session_data['workout_assignment_id']
            
        if 'session_date' in session_data:
            try:
                session.session_date = datetime.fromisoformat(session_data['session_date'].replace('Z', '+00:00'))
            except (ValueError, TypeError):
                try:
                    session.session_date = datetime.strptime(session_data['session_date'], '%Y-%m-%dT%H:%M:%S')
                except (ValueError, TypeError):
                    pass
                    
        if 'duration_minutes' in session_data:
            session.duration_minutes = session_data['duration_minutes']
            
        if 'notes' in session_data:
            session.notes = session_data['notes']
            
        if 'perceived_exertion' in session_data:
            session.perceived_exertion = session_data['perceived_exertion']
            
        if 'completed' in session_data:
            session.completed = session_data['completed']
        
        # Update exercise sets if provided
        if 'exercises' in session_data:
            # Optionally, handle exercise set updates
            # This is more complex as it involves potentially adding, updating, or
            # removing sets. Here's a simplified approach:
            
            # Option 1: Replace all sets (delete existing ones)
            if session_data.get('replace_sets', False):
                # Delete all existing sets for this session
                SetLog.query.filter_by(workout_session_id=session_id).delete()
                
                # Add new sets from the provided data
                for exercise_data in session_data['exercises']:
                    exercise_id = exercise_data.get('exercise_id')
                    
                    # Process sets for this exercise
                    sets_data = exercise_data.get('sets', [])
                    for i, set_data in enumerate(sets_data, 1):
                        set_number = set_data.get('set_number', i)
                        
                        set_log = SetLog(
                            workout_session_id=session.id,
                            exercise_id=exercise_id,
                            set_number=set_number,
                            reps=set_data.get('reps'),
                            weight=set_data.get('weight'),
                            weight_unit=set_data.get('weight_unit', 'lbs'),
                            duration_seconds=set_data.get('duration_seconds'),
                            distance=set_data.get('distance'),
                            distance_unit=set_data.get('distance_unit', 'miles'),
                            difficulty=set_data.get('difficulty'),
                            notes=set_data.get('notes')
                        )
                        
                        db.session.add(set_log)
            
            # Option 2: Selective update (more complex, would need to match on set ID)
            # This would involve updating existing sets or adding new ones based on IDs
        
        # Commit the changes
        db.session.commit()
        return session
    
    def delete_session_log(self, session_id):
        """
        Delete a workout session log and all its related sets.
        
        Args:
            session_id (int): ID of the workout session to delete
            
        Returns:
            bool: True if deletion was successful
        """
        session = WorkoutSession.query.get(session_id)
        if not session:
            return False
            
        db.session.delete(session)
        db.session.commit()
        return True
