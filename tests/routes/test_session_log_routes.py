import pytest
import json
from datetime import datetime, timedelta

class TestSessionLogRoutes:
    
    def test_create_session_log(self, client, auth_headers, test_user, test_exercises, test_workout_assignment):
        """Test POST /api/session-logs endpoint."""
        # Prepare test data
        session_data = {
            'workout_assignment_id': test_workout_assignment.id,
            'session_date': datetime.utcnow().isoformat(),
            'duration_minutes': 60,
            'notes': 'API test session',
            'perceived_exertion': 8,
            'completed': True,
            'exercises': [
                {
                    'exercise_id': test_exercises[0].id,
                    'sets': [
                        {
                            'set_number': 1,
                            'reps': 10,
                            'weight': 100,
                            'weight_unit': 'lbs'
                        },
                        {
                            'set_number': 2,
                            'reps': 8,
                            'weight': 120,
                            'weight_unit': 'lbs',
                            'notes': 'Increased weight'
                        }
                    ]
                }
            ]
        }
        
        # Make the API request
        response = client.post(
            '/api/session-logs',
            headers=auth_headers,
            json=session_data
        )
        
        # Check response
        assert response.status_code == 201
        data = json.loads(response.data)
        assert 'message' in data
        assert 'session' in data
        assert data['message'] == 'Workout session logged successfully'
        assert data['session']['notes'] == 'API test session'
        
        # Invalid request - missing exercise ID
        invalid_data = session_data.copy()
        invalid_data['exercises'] = [{'sets': [{'reps': 10}]}]
        
        response = client.post(
            '/api/session-logs',
            headers=auth_headers,
            json=invalid_data
        )
        assert response.status_code == 400
    
    def test_get_session_logs(self, client, auth_headers, test_user, test_workout_session):
        """Test GET /api/session-logs endpoint."""
        # Test with no filters
        response = client.get(
            '/api/session-logs',
            headers=auth_headers
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'sessions' in data
        assert 'pagination' in data
        assert data['pagination']['total'] >= 1
        
        # Test with date filter
        today = datetime.utcnow().strftime('%Y-%m-%d')
        response = client.get(
            f'/api/session-logs?start_date={today}',
            headers=auth_headers
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['pagination']['total'] >= 1
        
        # Test with completed filter
        response = client.get(
            '/api/session-logs?completed=true',
            headers=auth_headers
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['pagination']['total'] >= 1
        
        # Test pagination
        response = client.get(
            '/api/session-logs?page=1&per_page=5',
            headers=auth_headers
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['pagination']['per_page'] == 5
    
    def test_get_single_session_log(self, client, auth_headers, test_workout_session):
        """Test GET /api/session-logs/{id} endpoint."""
        # Get existing session
        response = client.get(
            f'/api/session-logs/{test_workout_session.id}',
            headers=auth_headers
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['id'] == test_workout_session.id
        assert data['user_id'] == test_workout_session.user_id
        assert 'exercises' in data
        assert len(data['exercises']) > 0
        
        # Check exercise data structure
        for exercise in data['exercises']:
            assert 'id' in exercise
            assert 'name' in exercise
            assert 'sets' in exercise
            assert len(exercise['sets']) > 0
            
            # Check set data structure
            for set_data in exercise['sets']:
                assert 'id' in set_data
                assert 'set_number' in set_data
        
        # Test non-existent session
        response = client.get(
            '/api/session-logs/9999',
            headers=auth_headers
        )
        assert response.status_code == 404
    
    def test_update_session_log(self, client, auth_headers, test_workout_session):
        """Test PUT /api/session-logs/{id} endpoint."""
        # Update session data
        update_data = {
            'notes': 'Updated via API',
            'duration_minutes': 55,
            'perceived_exertion': 9
        }
        
        response = client.put(
            f'/api/session-logs/{test_workout_session.id}',
            headers=auth_headers,
            json=update_data
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == 'Workout session updated successfully'
        assert data['session']['notes'] == 'Updated via API'
        assert data['session']['duration_minutes'] == 55
        assert data['session']['perceived_exertion'] == 9
        
        # Test non-existent session
        response = client.put(
            '/api/session-logs/9999',
            headers=auth_headers,
            json=update_data
        )
        assert response.status_code == 404
    
    def test_delete_session_log(self, client, auth_headers, test_workout_session):
        """Test DELETE /api/session-logs/{id} endpoint."""
        # First ensure the session exists
        response = client.get(
            f'/api/session-logs/{test_workout_session.id}',
            headers=auth_headers
        )
        assert response.status_code == 200
        
        # Delete the session
        response = client.delete(
            f'/api/session-logs/{test_workout_session.id}',
            headers=auth_headers
        )
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['message'] == 'Workout session deleted successfully'
        
        # Verify it's deleted
        response = client.get(
            f'/api/session-logs/{test_workout_session.id}',
            headers=auth_headers
        )
        assert response.status_code == 404
