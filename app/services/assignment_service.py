from app.models.workout_assignment import WorkoutAssignment
from app.models.user import User
from app.models.workout import Workout
from app import db
from sqlalchemy.exc import IntegrityError
from datetime import datetime
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
        user  = db.session.get(User, user_id)# User.query.get(user_id)
        if not user:
            return None, "User not found", 404
        
        # Verify workout exists
        workout = db.session.get(Workout, workout_id)#Workout.query.get(workout_id)
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
        assignment = db.session.get(WorkoutAssignment, assignment_id)#WorkoutAssignment.query.get(assignment_id)
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
        

    def remove_assignment(self, user_id, workout_id):
        """
        Remove a workout assignment for a user.
        
        Args:
            user_id (int): ID of the user
            workout_id (int): ID of the workout to unassign
            
        Returns:
            tuple: (bool success, message, status_code)
        """
        # Find the assignment
        assignment = WorkoutAssignment.query.filter_by(
            user_id=user_id,
            workout_id=workout_id,
            completed=False  # Only allow deletion of incomplete assignments
        ).first()
        
        if not assignment:
            return False, "Assignment not found or already completed", 404
        
        try:
            db.session.delete(assignment)
            db.session.commit()
            return True, "Workout successfully unassigned", 200
        except Exception as e:
            db.session.rollback()
            return False, f"Failed to remove assignment: {str(e)}", 500

    def replace_assignment(self, user_id, new_workout_id):
        """
        Replace current active assignment with a new one.
        
        Args:
            user_id (int): ID of the user
            new_workout_id (int): ID of the new workout to assign
            
        Returns:
            tuple: (WorkoutAssignment object, message, status_code)
        """
        # Verify workout exists
        new_workout = db.session.get(Workout,new_workout_id)#Workout.query.get(new_workout_id)
        if not new_workout:
            return None, "Workout not found", 404
        
        # Begin transaction
        try:
            # Find current active assignment
            current_assignment = WorkoutAssignment.query.filter_by(
                user_id=user_id,
                completed=False
            ).first()
            
            # If there's a current assignment, delete it
            if current_assignment:
                # If trying to assign the same workout, just return it
                if current_assignment.workout_id == new_workout_id:
                    return current_assignment, "User is already assigned to this workout", 200
                    
                db.session.delete(current_assignment)
            
            # Create new assignment
            new_assignment = WorkoutAssignment(
                user_id=user_id,
                workout_id=new_workout_id
            )
            
            db.session.add(new_assignment)
            db.session.commit()
            
            return new_assignment, "Workout assignment successfully replaced", 200
        except IntegrityError:
            db.session.rollback()
            return None, "Failed to replace assignment due to database constraint", 409
        except Exception as e:
            db.session.rollback()
            return None, f"Failed to replace assignment: {str(e)}", 500

    def get_active_assignment(self, user_id):
        """
        Get the current active assignment for a user.
        
        Args:
            user_id (int): ID of the user
            
        Returns:
            WorkoutAssignment or None: The active assignment, or None if none exists
        """
        return WorkoutAssignment.query.filter_by(
            user_id=user_id,
            completed=False
        ).first()