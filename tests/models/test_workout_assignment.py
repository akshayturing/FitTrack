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
# from datetime import datetime


class TestWorkoutAssignment:
    # def test_create_assignment(self, database):
    #     """Test creating a workout assignment"""
    #     # Create a user
    #     user = User(username="testuser", email="test@example.com")
    #     user.password = "password123"
    #     db.session.add(user)
    #     db.session.flush()  # Get the user ID without committing

    #     # Create a workout 
    #     # Changed 'name' to 'title' to match the model definition
    #     workout = Workout(
    #         title="Test Workout",  # CHANGED FROM name="Test Workout"
    #         user_id=user.id,
    #         description="Test workout description",
    #         workout_type="strength",
    #         duration=30,  # minutes
    #         difficulty_level="intermediate"
    #     )
    #     db.session.add(workout)
    #     db.session.flush()  # Get the workout ID without committing

    #     # Create a workout assignment
    #     assignment = WorkoutAssignment(
    #         user_id=user.id,
    #         workout_id=workout.id,
    #         assigned_date=datetime.datetime.utcnow(),
    #         is_active=True
    #     )
    #     db.session.add(assignment)
    #     db.session.commit()

    #     # Verify the assignment was created
    #     assignments = WorkoutAssignment.query.filter_by(user_id=user.id, is_active=True).all()
    #     assert len(assignments) == 1
    #     assert assignments[0].workout_id == workout.id
    #     assert assignments[0].is_active == True

    # def test_assignment_unique_constraint(self, database):
    #     """Test that a user cannot be assigned the same workout twice when both are active"""
    #     # Create a user
    #     user = User(username="testuser", email="test@example.com")
    #     user.password = "password123"
    #     db.session.add(user)
    #     db.session.flush()

    #     # Create a workout
    #     # Changed 'name' to 'title' to match the model definition
    #     workout = Workout(
    #         title="Test Workout1",  # CHANGED FROM name="Test Workout"
    #         user_id=user.id,
    #         description="Test workout description",
    #         workout_type="strength",
    #         duration=30,  # minutes
    #         difficulty_level="intermediate"
    #     )
    #     db.session.add(workout)
    #     db.session.flush()

    #     # Create a workout assignment
    #     assignment1 = WorkoutAssignment(
    #         user_id=user.id,
    #         workout_id=workout.id,
    #         assigned_date=datetime.datetime.utcnow(),
    #         is_active=True
    #     )
    #     db.session.add(assignment1)
    #     db.session.commit()

    #     existing = WorkoutAssignment.query.filter_by(
    #     user_id=user.id,
    #     workout_id=workout.id,
    #     is_active=True
    #     ).first()

    #     # if existing:
    #     #     # Manually trigger validation failure for test purposes
    #     #     raise ValueError("Active assignment already exists.")
    #     # Try to create another active assignment for the same user and workout
    #     assignment2 = WorkoutAssignment(
    #         user_id=user.id,
    #         workout_id=workout.id,
    #         assigned_date=datetime.datetime.utcnow(),
    #         is_active=True
    #     )
    #     db.session.add(assignment2)

    #     # This should raise an exception due to the unique constraint
    #     with pytest.raises(Exception):
    #         db.session.commit()

    #     # Rollback the session to clean up
    #     db.session.rollback()

    #     # If the first assignment is set to inactive, then we should be able to create another
    #     assignment1.is_active = False
    #     db.session.commit()

    #     # Now we can create another assignment
    #     assignment3 = WorkoutAssignment(
    #         user_id=user.id,
    #         workout_id=workout.id,
    #         assigned_date=datetime.datetime.utcnow(),
    #         is_active=True
    #     )
    #     db.session.add(assignment3)
        
    #     # This should not raise an exception
    #     db.session.commit()
        
    #     all_assignments = WorkoutAssignment.query.filter_by(
    #     user_id=user.id,
    #     workout_id=workout.id
    #     ).all()
    #     assert len(all_assignments) == 2  # One inactive, one active

    #     # This gets only the active one
    #     active_assignments = WorkoutAssignment.query.filter_by(
    #     user_id=user.id,
    #     workout_id=workout.id,
    #     is_active=True
    #     ).all()
    #     assert len(active_assignments) == 1

    def test_create_assignment(self, database):
        """Test creating a workout assignment"""
        # Create a user
        user = User(username="testuser", email="test@example.com")
        user.password = "password123"
        db.session.add(user)
        db.session.flush()

        # Create a workout
        workout = Workout(
            title="Test Workout",  
            user_id=user.id,
            description="Test workout description",
            workout_type="strength",
            duration=30,
            difficulty_level="intermediate"
        )
        db.session.add(workout)
        db.session.flush()

        # Check if assignment already exists and deactivate it
        existing_assignment = WorkoutAssignment.query.filter_by(
            user_id=user.id, 
            workout_id=workout.id,
            is_active=True
        ).first()
        
        if existing_assignment:
            existing_assignment.is_active = False
            db.session.commit()

        # Create a new workout assignment
        assignment = WorkoutAssignment(
            user_id=user.id,
            workout_id=workout.id,
            assigned_date=datetime.datetime.utcnow(),
            is_active=True
        )
        db.session.add(assignment)
        db.session.commit()

        # Verify the assignment was created
        assignments = WorkoutAssignment.query.filter_by(
            user_id=user.id, 
            workout_id=workout.id,
            is_active=True
        ).all()
        assert len(assignments) == 1
        assert assignments[0].workout_id == workout.id

    def test_assignment_unique_constraint(self, database):
        """Test that a user cannot be assigned the same workout twice when both are active"""
        # Create a user
        user = User(username="testuser", email="test@example.com")
        user.password = "password123"
        db.session.add(user)
        db.session.flush()

        # Create two different workouts
        workout1 = Workout(
            title="Test Workout 1",
            user_id=user.id,
            description="Test workout description 1",
            workout_type="strength",
            duration=30,
            difficulty_level="intermediate"
        )
        
        workout2 = Workout(
            title="Test Workout 2",  # Different workout
            user_id=user.id,
            description="Test workout description 2",
            workout_type="cardio",
            duration=45,
            difficulty_level="advanced"
        )
        
        db.session.add(workout1)
        db.session.add(workout2)
        db.session.flush()

        # Create assignments for different workouts - this should work
        assignment1 = WorkoutAssignment(
            user_id=user.id,
            workout_id=workout1.id,
            assigned_date=datetime.datetime.utcnow(),
            is_active=True
        )
        
        assignment2 = WorkoutAssignment(
            user_id=user.id,
            workout_id=workout2.id,  # Different workout
            assigned_date=datetime.datetime.utcnow(),
            is_active=True
        )
        
        db.session.add(assignment1)
        db.session.add(assignment2)
        db.session.commit()
        
        # Now try to create a duplicate assignment - this should fail
        duplicate_assignment = WorkoutAssignment(
            user_id=user.id,
            workout_id=workout1.id,  # Same as assignment1
            assigned_date=datetime.datetime.utcnow(),
            is_active=True
        )
        db.session.add(duplicate_assignment)

        # This should raise an exception due to the unique constraint
        with pytest.raises(Exception):
            db.session.commit()

        # Rollback the session to clean up
        db.session.rollback()
        
        # Verify we can add another assignment if the first is inactive
        assignment1.is_active = False
        db.session.commit()
        
        # Now try again with the first assignment inactive
        new_assignment = WorkoutAssignment(
            user_id=user.id,
            workout_id=workout1.id,
            assigned_date=datetime.datetime.utcnow(),
            is_active=True
        )
        db.session.add(new_assignment)
        db.session.commit()  # This should succeed now
        
        # Verify we have 3 total assignments
        assignments = WorkoutAssignment.query.filter_by(user_id=user.id).all()
        assert len(assignments) == 3