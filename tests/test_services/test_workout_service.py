import pytest
from app.services.workout_service import WorkoutService
from sqlalchemy.exc import SQLAlchemyError

def test_get_user_assigned_workouts(init_database):
    """Test getting workouts assigned to a user."""
    # Get test data
    test_user = init_database['users']['test_user']
    admin_user = init_database['users']['admin_user']
    
    # Get workouts for test user (should return 2 active workouts)
    workouts = WorkoutService.get_user_assigned_workouts(test_user.id)
    assert len(workouts) == 2
    assert init_database['workouts']['workout1'] in workouts
    assert init_database['workouts']['workout2'] in workouts
    
    # Make sure inactive workouts are not included
    assert init_database['workouts']['workout3'] not in workouts
    
    # Get workouts for admin (should return 1 workout)
    admin_workouts = WorkoutService.get_user_assigned_workouts(admin_user.id)
    assert len(admin_workouts) == 1
    assert init_database['workouts']['workout3'] in admin_workouts

def test_get_user_assigned_workouts_empty(init_database):
    """Test getting workouts when no workouts are assigned."""
    # Create a user with no workout assignments
    from app.models.user import User
    from app import db
    
    new_user = User(username='noworkouts', email='noworkouts@example.com')
    new_user.verify_password('password')
    db.session.add(new_user)
    db.session.commit()
    
    # User should have no workouts
    workouts = WorkoutService.get_user_assigned_workouts(new_user.id)
    assert len(workouts) == 0
    
def test_is_workout_assigned_to_user(init_database):
    """Test checking if a workout is assigned to a user."""
    test_user = init_database['users']['test_user']
    admin_user = init_database['users']['admin_user']
    workout1 = init_database['workouts']['workout1']
    workout3 = init_database['workouts']['workout3']
    
    # Test user should have workout1 assigned
    assert WorkoutService.is_workout_assigned_to_user(
        test_user.id, workout1.id) is True
    
    # Test user should not have workout3 assigned (inactive)
    assert WorkoutService.is_workout_assigned_to_user(
        test_user.id, workout3.id) is False
    
    # Admin user should have workout3 assigned
    assert WorkoutService.is_workout_assigned_to_user(
        admin_user.id, workout3.id) is True
    
    # Admin user should not have workout1 assigned
    assert WorkoutService.is_workout_assigned_to_user(
        admin_user.id, workout1.id) is False

def test_is_workout_assigned_to_user_nonexistent(init_database):
    """Test checking assignment with nonexistent IDs."""
    test_user = init_database['users']['test_user']
    
    # Test with nonexistent workout ID
    assert WorkoutService.is_workout_assigned_to_user(test_user.id, 999) is False
    
    # Test with nonexistent user ID
    assert WorkoutService.is_workout_assigned_to_user(999, 1) is False