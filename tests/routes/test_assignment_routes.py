import json
import pytest
from app import db
from app.models.workout_assignment import WorkoutAssignment
from app.models.workout import Workout
def test_create_assignment_success(client, auth_headers, test_workout):
    """Test creating an assignment via the API"""
    # Make the request
    response = client.post(
        '/api/assignments',
        headers=auth_headers['headers'],
        json={'workout_id': test_workout.id}
    )
    
    # Check response
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'assignment' in data
    assert data['assignment']['workout_id'] == test_workout.id
    
def test_create_assignment_missing_workout_id(client, auth_headers):
    """Test creating an assignment without workout_id"""
    # Make the request
    response = client.post(
        '/api/assignments',
        headers=auth_headers['headers'],
        json={}
    )
    
    # Check response
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert 'workout_id' in data['error'].lower()

def test_get_user_assignments(client, auth_headers, test_assignment):
    """Test getting user assignments via the API"""
    # Make the request
    response = client.get(
        '/api/assignments',
        headers=auth_headers['headers']
    )
    
    # Check response
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]['id'] == test_assignment.id

def test_delete_assignment(client, auth_headers, test_assignment):
    """Test deleting an assignment via the API"""
    # Make the request
    response = client.delete(
        f'/api/assignments/{test_assignment.workout_id}',
        headers=auth_headers['headers']
    )
    
    # Check response
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'message' in data
    assert 'success' in data['message'].lower()
    
    # Verify assignment is deleted
    with client.application.app_context():
        assignment = db.session.get(WorkoutAssignment, test_assignment.id)#WorkoutAssignment.query.get(test_assignment.id)
        assert assignment is None

def test_delete_nonexistent_assignment(client, auth_headers):
    """Test deleting a non-existent assignment"""
    # Make the request
    response = client.delete(
        '/api/assignments/999',
        headers=auth_headers['headers']
    )
    
    # Check response
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'error' in data
    assert 'not found' in data['error'].lower()

def test_replace_assignment(client, auth_headers, test_assignment):
    """Test replacing an assignment via the API"""
    with client.application.app_context():
        user = auth_headers['user']
        
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
        
        # Make the request
        response = client.put(
            '/api/assignments',
            headers=auth_headers['headers'],
            json={'workout_id': new_workout.id}
        )
        
        # Check response
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'assignment' in data
        assert data['assignment']['workout_id'] == new_workout.id
        
        # Verify old assignment is gone
        assignment = assignment = db.session.get(WorkoutAssignment, test_assignment.id)#WorkoutAssignment.query.get(test_assignment.id)
        assert assignment is None
        
        # Verify new assignment exists
        assignments = WorkoutAssignment.query.filter_by(
            user_id=user.id,
            workout_id=new_workout.id
        ).all()
        assert len(assignments) == 1

def test_mark_assignment_complete(client, auth_headers, test_assignment):
    """Test marking an assignment as complete via the API"""
    # Make the request
    response = client.put(
        f'/api/assignments/{test_assignment.id}/complete',
        headers=auth_headers['headers']
    )
    
    # Check response
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'assignment' in data
    assert data['assignment']['completed'] is True
    assert data['assignment']['completion_date'] is not None