import pytest
from app import db
from app.models.workout_assignment import WorkoutAssignment
from app.services.assignment_service import AssignmentService
from sqlalchemy.exc import IntegrityError
from app.models.workout import Workout
def test_create_assignment_success(app, auth_headers, test_workout):
    """Test creating an assignment successfully"""
    with app.app_context():
        user = auth_headers['user']
        service = AssignmentService()
        
        # Create assignment
        assignment, message, status_code = service.create_assignment(
            user.id, test_workout.id
        )
        
        # Check results
        assert status_code == 201
        assert "successfully" in message.lower()
        assert assignment is not None
        assert assignment.user_id == user.id
        assert assignment.workout_id == test_workout.id
        assert assignment.completed is False

def test_create_assignment_duplicate(app, auth_headers, test_assignment):
    """Test creating a duplicate assignment"""
    with app.app_context():
        user = auth_headers['user']
        service = AssignmentService()
        
        # Try to create duplicate assignment
        assignment, message, status_code = service.create_assignment(
            user.id, test_assignment.workout_id
        )
        
        # Check results
        assert status_code == 409
        assert "already assigned" in message.lower()
        assert assignment is None

def test_create_assignment_invalid_user(app, test_workout):
    """Test creating an assignment with invalid user"""
    with app.app_context():
        service = AssignmentService()
        
        # Try with non-existent user
        assignment, message, status_code = service.create_assignment(
            999, test_workout.id
        )
        
        # Check results
        assert status_code == 404
        assert "user not found" in message.lower()
        assert assignment is None

def test_create_assignment_invalid_workout(app, auth_headers):
    """Test creating an assignment with invalid workout"""
    with app.app_context():
        user = auth_headers['user']
        service = AssignmentService()
        
        # Try with non-existent workout
        assignment, message, status_code = service.create_assignment(
            user.id, 999
        )
        
        # Check results
        assert status_code == 404
        assert "workout not found" in message.lower()
        assert assignment is None

def test_remove_assignment_success(app, test_assignment):
    """Test removing an assignment successfully"""
    with app.app_context():
        service = AssignmentService()
        
        # Remove assignment
        success, message, status_code = service.remove_assignment(
            test_assignment.user_id, test_assignment.workout_id
        )
        
        # Check results
        assert status_code == 200
        assert success is True
        assert "successfully" in message.lower()
        
        # Verify it's gone from DB
        assignment  = db.session.get(WorkoutAssignment, test_assignment.id)#WorkoutAssignment.query.get(test_assignment.id)
        assert assignment is None

def test_remove_assignment_not_found(app, auth_headers):
    """Test removing a non-existent assignment"""
    with app.app_context():
        user = auth_headers['user']
        service = AssignmentService()
        
        # Try to remove non-existent assignment
        success, message, status_code = service.remove_assignment(
            user.id, 999
        )
        
        # Check results
        assert status_code == 404
        assert success is False
        assert "not found" in message.lower()

def test_replace_assignment_success(app, auth_headers, test_assignment, test_workout):
    """Test replacing an assignment successfully"""
    print("###################")
    with app.app_context():
        user = auth_headers['user']
        
        service = AssignmentService()
        
        # Create a second workout
        new_workout = Workout(
            user_id=user.id,
            title="New Test Workout",
            description="A new test workout",
            workout_type="cardio",
            difficulty_level="beginner",
            duration=20.0,
            category="cardio",
            is_public=True
        )
        
        db.session.add(new_workout)
        db.session.commit()
        
        # Replace assignment
        new_assignment, message, status_code = service.replace_assignment(
            user.id, new_workout.id
        )
        
        print(new_assignment, message, status_code)
        # Check results
        assert status_code == 200
        assert "successfully" in message.lower()
        assert new_assignment is not None
        assert new_assignment.workout_id == new_workout.id
        
        # Verify old assignment is gone
        old_assignment = db.session.get(WorkoutAssignment, test_assignment.id)#WorkoutAssignment.query.get(test_assignment.id)
        assert old_assignment is None

def test_replace_assignment_same_workout(app, auth_headers, test_assignment):
    """Test replacing with the same workout (no change)"""
    with app.app_context():
        user = auth_headers['user']
        service = AssignmentService()
        
        # Try to replace with same workout
        assignment, message, status_code = service.replace_assignment(
            user.id, test_assignment.workout_id
        )
        
        # Check results
        assert status_code == 200
        assert "already assigned" in message.lower()
        assert assignment is not None
        assert assignment.id == test_assignment.id

def test_replace_assignment_invalid_workout(app, auth_headers, test_assignment):
    """Test replacing with an invalid workout"""
    with app.app_context():
        user = auth_headers['user']
        service = AssignmentService()
        
        # Try to replace with non-existent workout
        assignment, message, status_code = service.replace_assignment(
            user.id, 999
        )
        
        # Check results
        assert status_code == 404
        assert "not found" in message.lower()
        assert assignment is None
        
        # Verify original assignment still exists
        original = db.session.get(WorkoutAssignment, test_assignment.id)#WorkoutAssignment.query.get(test_assignment.id)
        assert original is not None

def test_mark_assignment_complete(app, test_assignment):
    """Test marking an assignment as complete"""
    with app.app_context():
        service = AssignmentService()
        
        # Mark assignment complete
        assignment, message, status_code = service.mark_assignment_complete(
            test_assignment.id
        )
        
        # Check results
        assert status_code == 200
        assert "completed" in message.lower()
        assert assignment.completed is True
        assert assignment.completion_date is not None

def test_get_user_assignments(app, auth_headers, test_assignment):
    """Test getting a user's assignments"""
    with app.app_context():
        user = auth_headers['user']
        service = AssignmentService()
        
        # Get assignments (not completed)
        assignments = service.get_user_assignments(user.id, include_completed=False)
        
        # Check results
        assert len(assignments) == 1
        assert assignments[0].id == test_assignment.id
        
        # Mark as completed
        test_assignment.completed = True
        db.session.commit()
        
        # Get assignments (not completed) - should be empty
        assignments = service.get_user_assignments(user.id, include_completed=False)
        assert len(assignments) == 1
        
        # Get assignments (including completed)
        assignments = service.get_user_assignments(user.id, include_completed=True)
        assert len(assignments) == 1
