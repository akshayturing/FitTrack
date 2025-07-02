from app.models.workout_assignment import WorkoutAssignment
from app.models.user import User
from app.models.workout import Workout
from app import db
from sqlalchemy.exc import IntegrityError

class AssignmentService:
    def create_assignment(self, user_id, workout_id):
        """
        Create a new workout assignment for a user.
        
        Args:
            user_id (int): ID of the user
            workout_id (int): ID of the workout to assign
            
        Returns:
            tuple: (WorkoutAssignment object, message, status_code)
        """
        # Verify user exists
        user = User.query.get(user_id)
        if not user:
            return None, "User not found", 404
        
        # Verify workout exists
        workout = Workout.query.get(workout_id)
        if not workout:
            return None, "Workout not found", 404
        
        # Check if assignment already exists
        existing_assignment = WorkoutAssignment.query.filter_by(
            user_id=user_id, 
            workout_id=workout_id
        ).first()
        
        if existing_assignment:
            return None, "This workout is already assigned to the user", 409
        
        # Create a new assignment
        assignment = WorkoutAssignment(user_id=user_id, workout_id=workout_id)
        
        try:
            db.session.add(assignment)
            db.session.commit()
            return assignment, "Workout assigned successfully", 201
        except IntegrityError:
            db.session.rollback()
            return None, "This workout is already assigned to the user", 409
        except Exception as e:
            db.session.rollback()
            return None, f"Failed to create assignment: {str(e)}", 500
    
    def get_user_assignments(self, user_id, include_completed=False):
        """Get all assignments for a specific user."""
        query = WorkoutAssignment.query.filter_by(user_id=user_id)
        
        if not include_completed:
            query = query.filter_by(completed=False)
            
        return query.all()
    
    def mark_assignment_complete(self, assignment_id):
        """Mark an assignment as completed."""
        assignment = WorkoutAssignment.query.get(assignment_id)
        if not assignment:
            return None, "Assignment not found", 404
            
        assignment.completed = True
        assignment.completion_date = datetime.utcnow()
        
        try:
            db.session.commit()
            return assignment, "Assignment marked as completed", 200
        except Exception as e:
            db.session.rollback()
            return None, f"Failed to update assignment: {str(e)}", 500