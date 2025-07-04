# # import pytest
# # from app import create_app, db
# # from app.models.user import User
# # from app.models.workout import Workout
# # from app.models.workout_assignment import WorkoutAssignment
# # from flask_jwt_extended import create_access_token
# # import sys
# # import os
# # sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# # @pytest.fixture
# # def app():
# #     """Create and configure a Flask app for testing"""
# #     app = create_app('testing')
    
# #     # Create a test database and apply the schema
# #     with app.app_context():
# #         db.create_all()
# #         yield app
# #         db.session.remove()
# #         db.drop_all()

# # @pytest.fixture
# # def client(app):
# #     """A test client for the app"""
# #     return app.test_client()

# # @pytest.fixture
# # def runner(app):
# #     """A test CLI runner for the app"""
# #     return app.test_cli_runner()

# # @pytest.fixture
# # def auth_headers(app):
# #     """Auth headers for test user"""
# #     with app.app_context():
# #         # Create test user
# #         user = User(
# #             username="testuser",
# #             email="test@example.com"
# #         )
# #         user.password = "TestPassword123!"
# #         db.session.add(user)
# #         db.session.commit()
        
# #         # Generate token
# #         token = create_access_token(identity=user.id)
# #         headers = {
# #             'Authorization': f'Bearer {token}',
# #             'Content-Type': 'application/json'
# #         }
        
# #         # Return both the user and headers
# #         return {'user': user, 'headers': headers}

# # @pytest.fixture
# # def test_workout(app, auth_headers):
# #     """Create a test workout"""
# #     with app.app_context():
# #         user = auth_headers['user']
        
# #         workout = Workout(
# #             user_id=user.id,
# #             title="Test Workout",
# #             description="A test workout description",
# #             workout_type="strength",
# #             difficulty_level="intermediate",
# #             duration=30.0,
# #             category="strength",
# #             is_public=True
# #         )
        
# #         db.session.add(workout)
# #         db.session.commit()
        
# #         return workout

# # @pytest.fixture
# # def test_assignment(app, auth_headers, test_workout):
# #     """Create a test workout assignment"""
# #     with app.app_context():
# #         user = auth_headers['user']
        
# #         assignment = WorkoutAssignment(
# #             user_id=user.id,
# #             workout_id=test_workout.id
# #         )
        
# #         db.session.add(assignment)
# #         db.session.commit()
        
# #         return assignment
# # tests/conftest.py
# import pytest
# from app import create_app, db
# from app.models.user import User
# from app.models.workout import Workout
# from app.models.workout_assignment import WorkoutAssignment
# from flask_jwt_extended import create_access_token
# from sqlalchemy.orm import scoped_session, sessionmaker
# @pytest.fixture
# def app():
#     """Create and configure a Flask app for testing"""
#     app = create_app('testing')
    
#     # Create a test database and apply the schema
#     with app.app_context():
#         db.create_all()
#         yield app
#         db.session.remove()
#         db.drop_all()

# @pytest.fixture
# def client(app):
#     """A test client for the app"""
#     return app.test_client()

# @pytest.fixture
# def session(app):
#     """Create a new database session for tests"""
#     with app.app_context():
#         connection = db.engine.connect()
#         transaction = connection.begin()
        
#         # Create a session bound to the connection
#         ScopedSession = scoped_session(sessionmaker(bind=connection))
#         session = ScopedSession()
        
#         # Replace the global session with our test session
#         # old_session = db.session
#         # db.session = session
        
#         yield session
        
#         # Rollback the transaction and restore the original session
#         transaction.rollback()
#         connection.close()
#         ScopedSession.remove()
#         # db.session = old_session

# @pytest.fixture
# def auth_headers(app, session):
#     """Auth headers for test user"""
#     with app.app_context():
#         # Create test user
#         user = User(
#             username="testuser89",
#             email="tes89t@example.com"
#         )
#         user.password = "TestPassword123!"
#         session.add(user)
#         session.commit()
        
#         # Generate token
#         token = create_access_token(identity=user.id)
#         headers = {
#             'Authorization': f'Bearer {token}',
#             'Content-Type': 'application/json'
#         }
        
#         # Return both the user and headers
#         return {'user': user, 'headers': headers}

# @pytest.fixture
# def test_workout(app, session, auth_headers):
#     """Create a test workout"""
#     with app.app_context():
#         user = auth_headers['user']
        
#         workout = Workout(
#             user_id=user.id,
#             title="Test Workout",
#             description="A test workout description",
#             workout_type="strength",
#             difficulty_level="intermediate",
#             duration=30.0,
#             category="strength",
#             is_public=True
#         )
        
#         session.add(workout)
#         session.commit()
#         # Refresh the instance to ensure it's bound to the session
#         session.refresh(workout)
        
#         return workout

# @pytest.fixture
# def test_assignment(app, session, auth_headers, test_workout):
#     """Create a test workout assignment"""
#     print("######################")
#     with app.app_context():
#         user = auth_headers['user']
        
#         assignment = WorkoutAssignment(
#             user_id=user.id,
#             workout_id=test_workout.id
#         )
        
#         session.add(assignment)
#         session.commit()
#         # Refresh the instance to ensure it's bound to the session
#         session.refresh(assignment)
        
#         return assignment

import pytest
from app import create_app, db
from app.models.user import User
from app.models.workout import Workout
from app.models.workout_assignment import WorkoutAssignment
from app.models.exercise import Exercise
from flask_login import login_user

@pytest.fixture
def app():
    """Create application for the tests."""
    app = create_app('testing')
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False
    
    # Create app context for tests
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """Create a test CLI runner for the app."""
    return app.test_cli_runner()

@pytest.fixture
def init_database(app):
    """Initialize test database with sample data."""
    # Create test users
    test_user = User(username='testuser', email='test@example.com', password='password123', is_admin=False)
    # test_user.set_password('password123')
    
    admin_user = User(username='admin', email='admin@example.com',password='adminpass', is_admin=True)
    # admin_user.set_password('adminpass')
    
    # Create test workouts
    workout1 = Workout(
        title='Beginner Strength Training',
        description='A full body workout for beginners',
        workout_type='strength',
        difficulty_level='beginner',
        duration=30
        # equipment_required=False
    )
    
    workout2 = Workout(
        title='HIIT Cardio Blast',
        description='High intensity interval training',
        workout_type='cardio',
        difficulty_level='intermediate',
        duration=45
        # equipment_required=True
    )
    
    workout3 = Workout(
        title='Advanced Flexibility',
        description='Deep stretches for advanced practitioners',
        workout_type='flexibility',
        difficulty_level='advanced',
        duration=60
        # equipment_required=False
    )
    
    # Create exercises for workouts
    exercise1 = Exercise(
        name='Push-ups',
        description='Basic push-ups',
        default_sets=3,
        default_reps=10,

        type = 'strength'
        # workout=workout1
    )
    
    exercise2 = Exercise(
        name='Squats',
        description='Basic squats',
        default_sets=3,
        default_reps=15,
        type = 'strength'
        # workout=workout1
    )
    
    exercise3 = Exercise(
        name='Burpees',
        description='Full burpees',
        default_sets=4,
        default_reps=20,
        type = 'strength'
        # workout=workout2
    )
    
    # Create workout assignments
    assignment1 = WorkoutAssignment(
        user_id = 1,
        workout_id = 1
        # user=test_user,
        # workout=workout1,
        # is_active=True
    )
    
    assignment2 = WorkoutAssignment(
        user_id = 2,
        workout_id = 2
        # user=test_user,
        # workout=workout2,
        # is_active=True
    )
    
    assignment3 = WorkoutAssignment(
        user_id = 3,
        workout_id = 3
        # user=admin_user,
        # workout=workout3,
        # is_active=True
    )
    
    assignment4 = WorkoutAssignment(
        user_id = 4,
        workout_id = 4
        # user=test_user,
        # workout=workout3,
        # is_active=False  # Inactive assignment
    )
    
    # Add to db and commit
    db.session.add_all([
        test_user, admin_user, 
        workout1, workout2, workout3,
        exercise1, exercise2, exercise3,
        assignment1, assignment2, assignment3, assignment4
    ])
    db.session.commit()
    
    return {
        'users': {'test_user': test_user, 'admin_user': admin_user},
        'workouts': {
            'workout1': workout1, 
            'workout2': workout2, 
            'workout3': workout3
        }
    }

@pytest.fixture
def logged_in_client(client, init_database):
    """Create a client with a logged in test user."""
    with client.session_transaction() as session:
        # Log in the test user
        user = init_database['users']['test_user']
        login_user(user)
        session['user_id'] = user.id
    return client

@pytest.fixture
def logged_in_admin(client, init_database):
    """Create a client with a logged in admin user."""
    with client.session_transaction() as session:
        # Log in the admin user
        user = init_database['users']['admin_user']
        login_user(user)
        session['user_id'] = user.id
    return client