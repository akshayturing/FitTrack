import pytest
from app.services.session_log_service import SessionLogService
from app.models.workout_log import WorkoutSession, SetLog
from datetime import datetime, timedelta

class TestSessionLogService:
    
    def test_create_session_log(self, app, test_user, test_exercises, test_workout_assignment):
        """Test creating a new workout session with exercises and sets."""
        with app.app_context():
            service = SessionLogService()
            
            # Prepare test data
            session_data = {
                'workout_assignment_id': test_workout_assignment.id,
                'session_date': datetime.utcnow().isoformat(),
                'duration_minutes': 60,
                'notes': 'Test session',
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
                    },
                    {
                        'exercise_id': test_exercises[1].id,
                        'sets': [
                            {
                                'set_number': 1,
                                'duration_seconds': 60
                            }
                        ]
                    }
                ]
            }
            
            # Create the session
            result = service.create_session_log(test_user.id, session_data)
            
            # Verify results
            assert result is not None
            assert result.user_id == test_user.id
            assert result.workout_assignment_id == test_workout_assignment.id
            assert result.duration_minutes == 60
            assert result.notes == 'Test session'
            assert result.perceived_exertion == 8
            assert result.completed == True
            
            # Verify sets were created
            assert len(result.set_logs) == 3  # Two sets for first exercise, one for second
            
            # Verify bench press sets
            bench_press_sets = [s for s in result.set_logs if s.exercise_id == test_exercises[0].id]
            assert len(bench_press_sets) == 2
            assert bench_press_sets[0].reps == 10
            assert bench_press_sets[0].weight == 100
            assert bench_press_sets[1].reps == 8
            assert bench_press_sets[1].weight == 120
            assert bench_press_sets[1].notes == 'Increased weight'
            
            # Verify plank set
            plank_sets = [s for s in result.set_logs if s.exercise_id == test_exercises[1].id]
            assert len(plank_sets) == 1
            assert plank_sets[0].duration_seconds == 60
    
    def test_get_session_logs_with_filters(self, app, test_user, test_workout_session):
        """Test retrieving workout sessions with filters."""
        with app.app_context():
            service = SessionLogService()
            
            # Test with user_id filter
            result = service.get_session_logs({'user_id': test_user.id}, page=1, per_page=10)
            assert result['total'] >= 1
            assert any(s['id'] == test_workout_session.id for s in result['items'])
            
            # Test with date filters
            today = datetime.utcnow().date()
            yesterday = today - timedelta(days=1)
            tomorrow = today + timedelta(days=1)
            
            # Should find sessions
            result = service.get_session_logs({
                'user_id': test_user.id,
                'start_date': yesterday,
                'end_date': tomorrow
            }, page=1, per_page=10)
            assert result['total'] >= 1
            
            # Should not find sessions
            result = service.get_session_logs({
                'user_id': test_user.id,
                'start_date': tomorrow
            }, page=1, per_page=10)
            assert result['total'] == 0
            
            # Test with completion status
            result = service.get_session_logs({
                'user_id': test_user.id,
                'completed': True
            }, page=1, per_page=10)
            assert result['total'] >= 1
            
            result = service.get_session_logs({
                'user_id': test_user.id,
                'completed': False
            }, page=1, per_page=10)
            assert result['total'] == 0  # Our test session is completed
    
    def test_get_session_log_by_id(self, app, test_workout_session):
        """Test retrieving a single session by ID."""
        with app.app_context():
            service = SessionLogService()
            
            # Get existing session
            session = service.get_session_log_by_id(test_workout_session.id)
            assert session is not None
            assert session.id == test_workout_session.id
            
            # Try non-existent session
            session = service.get_session_log_by_id(9999)
            assert session is None
    
    def test_update_session_log(self, app, test_workout_session):
        """Test updating a workout session."""
        with app.app_context():
            service = SessionLogService()
            
            # Update session metadata
            update_data = {
                'notes': 'Updated test notes',
                'duration_minutes': 50,
                'perceived_exertion': 9,
                'completed': True
            }
            
            updated = service.update_session_log(test_workout_session.id, update_data)
            
            # Verify updates applied
            assert updated.notes == 'Updated test notes'
            assert updated.duration_minutes == 50
            assert updated.perceived_exertion == 9
            assert updated.completed == True
    
    def test_delete_session_log(self, app, test_workout_session):
        """Test deleting a workout session."""
        with app.app_context():
            service = SessionLogService()
            
            # Count set logs before deletion
            set_count_before = SetLog.query.filter_by(workout_session_id=test_workout_session.id).count()
            assert set_count_before > 0
            
            # Delete the session
            result = service.delete_session_log(test_workout_session.id)
            assert result is True
            
            # Verify session is deleted
            session = WorkoutSession.query.get(test_workout_session.id)
            assert session is None
            
            # Verify cascade delete of set logs
            set_count_after = SetLog.query.filter_by(workout_session_id=test_workout_session.id).count()
            assert set_count_after == 0
            
            # Try deleting non-existent session
            result = service.delete_session_log(9999)
            assert result is False
