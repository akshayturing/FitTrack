import pytest
import json
from flask import url_for

def test_dashboard_endpoint_requires_login(client):
    """Test that the dashboard page requires login."""
    response = client.get('/dashboard')
    # Should redirect to login page
    assert response.status_code == 302
    assert 'login' in response.headers['Location']

def test_dashboard_endpoint_logged_in(logged_in_client):
    """Test accessing the dashboard when logged in."""
    response = logged_in_client.get('/dashboard')
    assert response.status_code == 200
    # Verify the HTML contains expected content
    assert b'Your Workout Dashboard' in response.data
    assert b'id="workoutList"' in response.data

def test_user_workouts_endpoint_authentication(client, init_database):
    """Test that the workouts API enforces authentication."""
    test_user = init_database['users']['test_user']
    endpoint = f'/api/users/{test_user.id}/workouts'
    
    # Unauthorized access should be redirected or denied
    response = client.get(endpoint)
    assert response.status_code in [302, 401, 403]

def test_user_workouts_endpoint_own_data(logged_in_client, init_database):
    """Test that users can access their own workout data."""
    test_user = init_database['users']['test_user']
    endpoint = f'/api/users/{test_user.id}/workouts'
    
    response = logged_in_client.get(endpoint)
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'workouts' in data
    assert len(data['workouts']) == 2
    
    # Check that we have the right workout names
    workout_names = [w['name'] for w in data['workouts']]
    assert 'Beginner Strength Training' in workout_names
    assert 'HIIT Cardio Blast' in workout_names
    
    # Check that exercise data is included
    assert len(data['workouts'][0]['exercises']) > 0

def test_user_workouts_endpoint_other_user(logged_in_client, init_database):
    """Test that users cannot access other users' workout data."""
    admin_user = init_database['users']['admin_user']
    endpoint = f'/api/users/{admin_user.id}/workouts'
    
    response = logged_in_client.get(endpoint)
    assert response.status_code == 403
    
    data = json.loads(response.data)
    assert 'error' in data

def test_admin_access_any_user_workouts(logged_in_admin, init_database):
    """Test that admins can access any user's workout data."""
    test_user = init_database['users']['test_user']
    endpoint = f'/api/users/{test_user.id}/workouts'
    
    response = logged_in_admin.get(endpoint)
    assert response.status_code == 200
    
    data = json.loads(response.data)
    assert 'workouts' in data
    assert len(data['workouts']) == 2

def test_start_workout_session_endpoint_requires_login(client, init_database):
    """Test that starting a workout requires login."""
    workout1 = init_database['workouts']['workout1']
    response = client.get(f'/workout-session/start/{workout1.id}')
    # Should redirect to login
    assert response.status_code == 302
    assert 'login' in response.headers['Location']

def test_start_workout_session_endpoint_assigned(logged_in_client, init_database):
    """Test starting a workout session for an assigned workout."""
    workout1 = init_database['workouts']['workout1']
    response = logged_in_client.get(f'/workout-session/start/{workout1.id}')
    assert response.status_code == 200
    
def test_start_workout_session_endpoint_not_assigned(logged_in_client, init_database):
    """Test starting a workout session for a workout not assigned to user."""
    workout3 = init_database['workouts']['workout3']
    response = logged_in_client.get(f'/workout-session/start/{workout3.id}')
    assert response.status_code == 404

def test_start_workout_session_endpoint_nonexistent(logged_in_client):
    """Test starting a workout session with an invalid workout ID."""
    response = logged_in_client.get('/workout-session/start/999')
    assert response.status_code == 404