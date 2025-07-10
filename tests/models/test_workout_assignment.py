import pytest
from app import db
from app.models.workout_assignment import WorkoutAssignment
from sqlalchemy.exc import IntegrityError

def test_create_assignment(app, auth_headers, test_workout):
    """Test creating a workout assignment"""
    with app.app_context():
        user = auth_headers['user']
        
        # Create assignment
        assignment = WorkoutAssignment(
            user_id=user.id,
            workout_id=test_workout.id
        )
        
        db.session.add(assignment)
        db.session.commit()
        
        # Verify it was created
        assert assignment.id is not None
        assert assignment.user_id == user.id
        assert assignment.workout_id == test_workout.id
        assert assignment.completed is False
        assert assignment.completion_date is None
        
        # Test to_dict method
        assignment_dict = assignment.to_dict()
        assert assignment_dict['id'] == assignment.id
        assert assignment_dict['user_id'] == user.id
        assert assignment_dict['workout_id'] == test_workout.id
        assert assignment_dict['completed'] is False

def test_assignment_unique_constraint(app, auth_headers, test_workout):
    """Test unique constraint on user_id and workout_id"""
    with app.app_context():
        user = auth_headers['user']
        
        # Create first assignment
        assignment1 = WorkoutAssignment(
            user_id=user.id,
            workout_id=test_workout.id
        )
        
        db.session.add(assignment1)
        db.session.commit()
        
        # Try to create duplicate assignment
        assignment2 = WorkoutAssignment(
            user_id=user.id,
            workout_id=test_workout.id
        )
        
        db.session.add(assignment2)
        
        # Should raise IntegrityError
        with pytest.raises(IntegrityError):
            db.session.commit()
            
        # Rollback for cleanup
        db.session.rollback()

def test_cascade_delete_user(app, auth_headers, test_assignment):
    """Test cascade delete when user is deleted"""
    with app.app_context():
        user = auth_headers['user']
        assignment_id = test_assignment.id
        
        # Delete the user
        db.session.delete(user)
        db.session.commit()
        
        # Assignment should be deleted too (cascade)
        assignment = assignment = db.session.get(WorkoutAssignment, assignment_id)#WorkoutAssignment.query.get(assignment_id)
        assert assignment is None

def test_cascade_delete_workout(app, test_assignment, test_workout):
    """Test cascade delete when workout is deleted"""
    with app.app_context():
        assignment_id = test_assignment.id
        
        # Delete the workout
        db.session.delete(test_workout)
        db.session.commit()
        
        # Assignment should be deleted too (cascade)
        assignment = assignment = db.session.get(WorkoutAssignment, assignment_id)#WorkoutAssignment.query.get(assignment_id)
        assert assignment is None
