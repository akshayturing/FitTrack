# import pytest
# from app import db
# from app.models.workout_assignment import WorkoutAssignment
# from sqlalchemy.exc import IntegrityError

# def test_create_assignment(app, auth_headers, test_workout):
#     """Test creating a workout assignment"""
#     with app.app_context():
#         user = auth_headers['user']
        
#         # Create assignment
#         assignment = WorkoutAssignment(
#             user_id=user.id,
#             workout_id=test_workout.id
#         )
        
#         db.session.add(assignment)
#         db.session.commit()
        
#         # Verify it was created
#         assert assignment.id is not None
#         assert assignment.user_id == user.id
#         assert assignment.workout_id == test_workout.id
#         assert assignment.completed is False
#         assert assignment.completion_date is None
        
#         # Test to_dict method
#         assignment_dict = assignment.to_dict()
#         assert assignment_dict['id'] == assignment.id
#         assert assignment_dict['user_id'] == user.id
#         assert assignment_dict['workout_id'] == test_workout.id
#         assert assignment_dict['completed'] is False

# def test_assignment_unique_constraint(app, auth_headers, test_workout):
#     """Test unique constraint on user_id and workout_id"""
#     with app.app_context():
#         user = auth_headers['user']
        
#         # Create first assignment
#         assignment1 = WorkoutAssignment(
#             user_id=user.id,
#             workout_id=test_workout.id
#         )
        
#         db.session.add(assignment1)
#         db.session.commit()
        
#         # Try to create duplicate assignment
#         assignment2 = WorkoutAssignment(
#             user_id=user.id,
#             workout_id=test_workout.id
#         )
        
#         db.session.add(assignment2)
        
#         # Should raise IntegrityError
#         with pytest.raises(IntegrityError):
#             db.session.commit()
            
#         # Rollback for cleanup
#         db.session.rollback()

# # def test_cascade_delete_user(app, auth_headers, test_assignment):
# #     """Test cascade delete when user is deleted"""
# #     with app.app_context():
# #         user = auth_headers['user']
# #         assignment_id = test_assignment.id
        
# #         # Delete the user
# #         db.session.delete(user)
# #         db.session.commit()
        
# #         # Assignment should be deleted too (cascade)
# #         assignment = assignment = db.session.get(WorkoutAssignment, assignment_id)#WorkoutAssignment.query.get(assignment_id)
# #         assert assignment is None

# # def test_cascade_delete_workout(app, test_assignment, test_workout):
# #     """Test cascade delete when workout is deleted"""
# #     with app.app_context():
# #         assignment_id = test_assignment.id
        
# #         # Delete the workout
# #         db.session.delete(test_workout)
# #         db.session.commit()
        
# #         # Assignment should be deleted too (cascade)
# #         assignment = assignment = db.session.get(WorkoutAssignment, assignment_id)#WorkoutAssignment.query.get(assignment_id)
# #         assert assignment is None
# Updated test_workout_assignment.py

import pytest
from app.models.user import User
from app.models.workout import Workout
from app.models.workout_assignment import WorkoutAssignment
from app import db
import datetime

class TestWorkoutAssignment:
    def test_create_assignment(self, database):
        """Test creating a workout assignment"""
        # Create a user
        user = User(username="testuser", email="test@example.com")
        user.password = "password123"
        db.session.add(user)
        db.session.flush()  # Get the user ID without committing

        # Create a workout 
        # Changed 'name' to 'title' to match the model definition
        workout = Workout(
            title="Test Workout",  # CHANGED FROM name="Test Workout"
            user_id=user.id,
            description="Test workout description",
            workout_type="strength",
            duration=30,  # minutes
            difficulty_level="intermediate"
        )
        db.session.add(workout)
        db.session.flush()  # Get the workout ID without committing

        # Create a workout assignment
        assignment = WorkoutAssignment(
            user_id=user.id,
            workout_id=workout.id,
            assigned_date=datetime.datetime.utcnow(),
            is_active=True
        )
        db.session.add(assignment)
        db.session.commit()

        # Verify the assignment was created
        assignments = WorkoutAssignment.query.filter_by(user_id=user.id).all()
        assert len(assignments) == 1
        assert assignments[0].workout_id == workout.id
        assert assignments[0].is_active == True

    def test_assignment_unique_constraint(self, database):
        """Test that a user cannot be assigned the same workout twice when both are active"""
        # Create a user
        user = User(username="testuser", email="test@example.com")
        user.password = "password123"
        db.session.add(user)
        db.session.flush()

        # Create a workout
        # Changed 'name' to 'title' to match the model definition
        workout = Workout(
            title="Test Workout",  # CHANGED FROM name="Test Workout"
            user_id=user.id,
            description="Test workout description",
            workout_type="strength",
            duration=30,  # minutes
            difficulty_level="intermediate"
        )
        db.session.add(workout)
        db.session.flush()

        # Create a workout assignment
        assignment1 = WorkoutAssignment(
            user_id=user.id,
            workout_id=workout.id,
            assigned_date=datetime.datetime.utcnow(),
            is_active=True
        )
        db.session.add(assignment1)
        db.session.commit()

        # Try to create another active assignment for the same user and workout
        assignment2 = WorkoutAssignment(
            user_id=user.id,
            workout_id=workout.id,
            assigned_date=datetime.datetime.utcnow(),
            is_active=True
        )
        db.session.add(assignment2)

        # This should raise an exception due to the unique constraint
        with pytest.raises(Exception):
            db.session.commit()

        # Rollback the session to clean up
        db.session.rollback()

        # If the first assignment is set to inactive, then we should be able to create another
        assignment1.is_active = False
        db.session.commit()

        # Now we can create another assignment
        assignment3 = WorkoutAssignment(
            user_id=user.id,
            workout_id=workout.id,
            assigned_date=datetime.datetime.utcnow(),
            is_active=True
        )
        db.session.add(assignment3)
        
        # This should not raise an exception
        db.session.commit()
        
        # Verify we have two assignments for the user, but only one is active
        assignments = WorkoutAssignment.query.filter_by(user_id=user.id).all()
        assert len(assignments) == 2
        active_assignments = WorkoutAssignment.query.filter_by(user_id=user.id, is_active=True).all()
        assert len(active_assignments) == 1
