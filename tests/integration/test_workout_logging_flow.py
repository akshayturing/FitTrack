import pytest
import json
from datetime import datetime

class TestWorkoutLoggingFlow:
    """Test full workout logging workflow."""
    
    def test_complete_workout_flow(self, client, auth_headers, test_user, test_exercises):
        """
        Test the complete workflow of:
        1. Creating a workout session
        2. Retrieving it
        3. Updating it
        4. Deleting it
        """
        # 1. Create a workout session
        session_data = {
            'session_date': datetime.utcnow().isoformat(),
            'duration_minutes': 75,
            'notes': 'Complete flow test',
            'perceived_exertion': 8,
            'completed': False,
            'exercises': [
                {
                    'exercise_id': test_exercises[0].id,
                    'sets': [
                        {
                            'set_number': 1,
                            'reps': 10,
                            'weight': 135,
                            'weight_unit': 'lbs',
                            'notes': 'Warm-up'
                        },
                        {
                            'set_number': 2,
                            'reps': 8,
                            'weight': 185,
                            'weight_unit': 'lbs'
                        }
                    ]
                },
                {
                    'exercise_id': test_exercises[2].id,
                    'sets': [
                        {
                            'set_number': 1,
                            'distance': 2.0,
                            'duration_seconds': 1200,
                            'distance_unit': 'miles',
                            'notes': 'Steady pace'
                        }
                    ]
                }
            ]
        }
        
        create_response = client.post(
            '/api/session-logs',
            headers=auth_headers,
            json=session_data
        )
        assert create_response.status_code == 201
        create_data = json.loads(create_response.data)
        session_id = create_data['session']['id']
        
        # 2. Retrieve the created session
        get_response = client.get(
            f'/api/session-logs/{session_id}',
            headers=auth_headers
        )
        assert get_response.status_code == 200
        get_data = json.loads(get_response.data)
        
        # Verify data is correct
        assert get_data['notes'] == 'Complete flow test'
        assert get_data['duration_minutes'] == 75
        assert get_data['completed'] == False
        assert len(get_data['exercises']) == 2
        
        # Check first exercise details (bench press)
        bench_press = next(e for e in get_data['exercises'] if e['name'] == 'Bench Press')
        assert len(bench_press['sets']) == 2
        assert bench_press['sets'][0]['reps'] == 10
        assert bench_press['sets'][0]['weight'] == 135
        assert bench_press['sets'][0]['notes'] == 'Warm-up'
        
        # 3. Update the session
        update_data = {
            'completed': True,
            'notes': 'Completed and updated flow test',
            'perceived_exertion': 9
        }
        
        update_response = client.put(
            f'/api/session-logs/{session_id}',
            headers=auth_headers,
            json=update_data
        )
        assert update_response.status_code == 200
        
        # Verify update was applied
        get_after_update = client.get(
            f'/api/session-logs/{session_id}',
            headers=auth_headers
        )
        updated_data = json.loads(get_after_update.data)
        assert updated_data['completed'] == True
        assert updated_data['notes'] == 'Completed and updated flow test'
        assert updated_data['perceived_exertion'] == 9
        
        # 4. Delete the session
        delete_response = client.delete(
            f'/api/session-logs/{session_id}',
            headers=auth_headers
        )
        assert delete_response.status_code == 200
        
        # Verify deletion
        get_after_delete = client.get(
            f'/api/session-logs/{session_id}',
            headers=auth_headers
        )
        assert get_after_delete.status_code == 404
    
    def test_filtering_and_pagination(self, client, auth_headers, test_user, test_workout_session):
        """Test filtering and pagination of workout sessions."""
        # Create a second session to ensure we have multiple entries
        session_data = {
            'session_date': (datetime.utcnow() - timedelta(days=5)).isoformat(),
            'duration_minutes': 30,
            'notes': 'Older session for filtering test',
            'perceived_exertion': 6,
            'completed': True,
            'exercises': [
                {
                    'exercise_id': test_exercises[0].id,
                    'sets': [
                        {
                            'set_number': 1,
                            'reps': 12,
                            'weight': 95
                        }
                    ]
                }
            ]
        }
        
        client.post(
            '/api/session-logs',
            headers=auth_headers,
            json=session_data
        )
        
        # Test date filtering - get only recent sessions
        today = datetime.utcnow().strftime('%Y-%m-%d')
        yesterday = (datetime.utcnow() - timedelta(days=1)).strftime('%Y-%m-%d')
        
        recent_response = client.get(
            f'/api/session-logs?start_date={yesterday}',
            headers=auth_headers
        )
        recent_data = json.loads(recent_response.data)
        assert recent_data['pagination']['total'] >= 1
        assert all(s['session_date'].startswith(today[:4]) for s in recent_data['sessions'])
        
        # Test completed status filtering
        completed_response = client.get(
            '/api/session-logs?completed=true',
            headers=auth_headers
        )
        completed_data = json.loads(completed_response.data)
        assert completed_data['pagination']['total'] >= 1
        assert all(s['completed'] for s in completed_data['sessions'])
        
        # Test pagination - 1 item per page
        page1_response = client.get(
            '/api/session-logs?per_page=1&page=1',
            headers=auth_headers
        )
        page1_data = json.loads(page1_response.data)
        assert len(page1_data['sessions']) == 1
        assert page1_data['pagination']['current_page'] == 1
        
        page2_response = client.get(
            '/api/session-logs?per_page=1&page=2',
            headers=auth_headers
        )
        page2_data = json.loads(page2_response.data)
        
        # Make sure we got different sessions on different pages
        if page2_data['pagination']['total'] > 1:
            assert page2_data['sessions'][0]['id'] != page1_data['sessions'][0]['id']
