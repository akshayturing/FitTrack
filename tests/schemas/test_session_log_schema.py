# # import pytest
# # from app.schemas.session_log_schema import session_log_schema, session_logs_schema

# # class TestSessionLogSchema:
    
# #     def test_session_log_serialization(self, app, test_workout_session):
# #         """Test serializing a workout session."""
# #         with app.app_context():
# #             # Serialize a single session
# #             serialized = session_log_schema.dump(test_workout_session)
            
# #             # Check basic data
# #             assert serialized['id'] == test_workout_session.id
# #             assert serialized['user_id'] == test_workout_session.user_id
# #             assert serialized['duration_minutes'] == test_workout_session.duration_minutes
# #             assert serialized['notes'] == test_workout_session.notes
            
# #             # Check exercises
# #             assert 'exercises' in serialized
# #             assert len(serialized['exercises']) > 0
            
# #             # Check exercise structure - exercises should be grouped properly
# #             exercise = serialized['exercises'][0]
# #             assert 'id' in exercise
# #             assert 'name' in exercise
# #             assert 'sets' in exercise
# #             assert len(exercise['sets']) > 0
            
# #             # Check set data
# #             set_data = exercise['sets'][0]
# #             assert 'id' in set_data
# #             assert 'set_number' in set_data
            
# #             # Check that specific exercise types have appropriate fields
# #             for exercise in serialized['exercises']:
# #                 # For bench press, check reps and weight
# #                 if 'Bench Press' in exercise.get('name', ''):
# #                     assert any('reps' in s and 'weight' in s for s in exercise['sets'])
                    
# #                 # For plank, check duration_seconds
# #                 if 'Plank' in exercise.get('name', ''):
# #                     assert any('duration_seconds' in s for s in exercise['sets'])
                    
# #                 # For treadmill, check distance
# #                 if 'Treadmill' in exercise.get('name', ''):
# #                     assert any('distance' in s for s in exercise['sets'])
    
# #     def test_multiple_sessions_serialization(self, app, test_workout_session):
# #         """Test serializing multiple workout sessions."""
# #         with app.app_context():
# #             # Get all sessions for the test user
# #             sessions = [test_workout_session]
            
# #             # Serialize multiple sessions
# #             serialized = session_logs_schema.dump(sessions)
            
# #             # Check we have the right number
# #             assert len(serialized) == len(sessions)
            
# #             # Check first session matches
# #             assert serialized[0]['id'] == sessions[0].id

# import pytest
# from app.schemas.session_log_schema import session_log_schema, session_logs_schema
# from app.models.workout_log import WorkoutSession
# from sqlalchemy.orm import joinedload

# class TestSessionLogSchema:
    
#     def test_session_log_serialization(self, app, test_workout_session):
#         """Test serializing a workout session."""
#         with app.app_context():
#             # Query for the session with eager loading instead of using the fixture directly
#             session = WorkoutSession.query\
#                 .options(
#                     joinedload(WorkoutSession.user),
#                     joinedload(WorkoutSession.workout_assignment),
#                     joinedload(WorkoutSession.set_logs).joinedload(SetLog.exercise)
#                 )\
#                 .filter(WorkoutSession.id == test_workout_session.id)\
#                 .first()
            
#             # Serialize a single session with all related data already loaded
#             serialized = session_log_schema.dump(session)
            
#             # Rest of the assertions remain the same
#             assert serialized['id'] == session.id
#             assert serialized['user_id'] == session.user_id
#             # ...rest of assertions...
    
#     def test_multiple_sessions_serialization(self, app, test_workout_session):
#         """Test serializing multiple workout sessions."""
#         with app.app_context():
#             # Query with eager loading
#             sessions = WorkoutSession.query\
#                 .options(
#                     joinedload(WorkoutSession.user),
#                     joinedload(WorkoutSession.workout_assignment),
#                     joinedload(WorkoutSession.set_logs).joinedload(SetLog.exercise)
#                 )\
#                 .filter(WorkoutSession.id == test_workout_session.id)\
#                 .all()
            
#             # Serialize multiple sessions
#             serialized = session_logs_schema.dump(sessions)
            
#             # Check we have the right number
#             assert len(serialized) == len(sessions)
            
#             # Check first session matches
#             assert serialized[0]['id'] == sessions[0].id

import pytest
from app.schemas.session_log_schema import session_log_schema, session_logs_schema
from app.models.workout_log import WorkoutSession, SetLog
from sqlalchemy.orm import joinedload

class TestSessionLogSchema:
    
    def test_session_log_serialization(self, app, test_workout_session):
        """Test serializing a workout session with nested exercise and set data."""
        with app.app_context():
            # Query for the session with all relationships eagerly loaded
            session = WorkoutSession.query\
                .options(
                    joinedload(WorkoutSession.user),
                    joinedload(WorkoutSession.workout_assignment),
                    joinedload(WorkoutSession.set_logs).joinedload(SetLog.exercise)
                )\
                .filter_by(id=test_workout_session.id)\
                .first()

            serialized = session_log_schema.dump(session)

            # Basic assertions
            assert serialized['id'] == session.id
            assert serialized['user_id'] == session.user_id
            assert serialized['duration_minutes'] == session.duration_minutes
            assert serialized['notes'] == session.notes

            # Check nested exercises structure
            assert 'exercises' in serialized
            assert len(serialized['exercises']) > 0

            for exercise in serialized['exercises']:
                assert 'id' in exercise
                assert 'name' in exercise
                assert 'sets' in exercise
                assert len(exercise['sets']) > 0

                for s in exercise['sets']:
                    assert 'set_number' in s
                    assert 'id' in s

                # Domain-specific checks
                if 'Bench Press' in exercise.get('name', ''):
                    assert any('reps' in s and 'weight' in s for s in exercise['sets'])
                if 'Plank' in exercise.get('name', ''):
                    assert any('duration_seconds' in s for s in exercise['sets'])
                if 'Treadmill' in exercise.get('name', ''):
                    assert any('distance' in s for s in exercise['sets'])

    def test_multiple_sessions_serialization(self, app, test_workout_session):
        """Test serializing multiple workout sessions."""
        with app.app_context():
            sessions = WorkoutSession.query\
                .options(
                    joinedload(WorkoutSession.user),
                    joinedload(WorkoutSession.workout_assignment),
                    joinedload(WorkoutSession.set_logs).joinedload(SetLog.exercise)
                )\
                .filter_by(id=test_workout_session.id)\
                .all()

            serialized = session_logs_schema.dump(sessions)

            assert len(serialized) == len(sessions)
            assert serialized[0]['id'] == sessions[0].id
