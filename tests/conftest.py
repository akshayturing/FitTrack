# import pytest
# from app import create_app, db
# from app.models.user import User
# from app.models.workout import Workout
# from app.models.workout_assignment import WorkoutAssignment
# from flask_jwt_extended import create_access_token
# import sys
# import os
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
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
# def runner(app):
#     """A test CLI runner for the app"""
#     return app.test_cli_runner()

# @pytest.fixture
# def auth_headers(app):
#     """Auth headers for test user"""
#     with app.app_context():
#         # Create test user
#         user = User(
#             username="testuser",
#             email="test@example.com"
#         )
#         user.password = "TestPassword123!"
#         db.session.add(user)
#         db.session.commit()
        
#         # Generate token
#         token = create_access_token(identity=user.id)
#         headers = {
#             'Authorization': f'Bearer {token}',
#             'Content-Type': 'application/json'
#         }
        
#         # Return both the user and headers
#         return {'user': user, 'headers': headers}

# @pytest.fixture
# def test_workout(app, auth_headers):
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
        
#         db.session.add(workout)
#         db.session.commit()
        
#         return workout

# @pytest.fixture
# def test_assignment(app, auth_headers, test_workout):
#     """Create a test workout assignment"""
#     with app.app_context():
#         user = auth_headers['user']
        
#         assignment = WorkoutAssignment(
#             user_id=user.id,
#             workout_id=test_workout.id
#         )
        
#         db.session.add(assignment)
#         db.session.commit()
        
#         return assignment
# tests/conftest.py
import pytest
from app import create_app, db
from app.models.user import User
from app.models.workout import Workout
from app.models.workout_assignment import WorkoutAssignment
from flask_jwt_extended import create_access_token
from sqlalchemy.orm import scoped_session, sessionmaker
@pytest.fixture
def app():
    """Create and configure a Flask app for testing"""
    app = create_app('testing')
    
    # Create a test database and apply the schema
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """A test client for the app"""
    return app.test_client()

@pytest.fixture
def session(app):
    """Create a new database session for tests"""
    with app.app_context():
        connection = db.engine.connect()
        transaction = connection.begin()
        
        # Create a session bound to the connection
        ScopedSession = scoped_session(sessionmaker(bind=connection))
        session = ScopedSession()
        
        # Replace the global session with our test session
        # old_session = db.session
        # db.session = session
        
        yield session
        
        # Rollback the transaction and restore the original session
        transaction.rollback()
        connection.close()
        ScopedSession.remove()
        # db.session = old_session

@pytest.fixture
def auth_headers(app, session):
    """Auth headers for test user"""
    with app.app_context():
        # Create test user
        user = User(
            username="testuser89",
            email="tes89t@example.com"
        )
        user.password = "TestPassword123!"
        session.add(user)
        session.commit()
        
        # Generate token
        token = create_access_token(identity=user.id)
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        # Return both the user and headers
        return {'user': user, 'headers': headers}

@pytest.fixture
def test_workout(app, session, auth_headers):
    """Create a test workout"""
    with app.app_context():
        user = auth_headers['user']
        
        workout = Workout(
            user_id=user.id,
            title="Test Workout",
            description="A test workout description",
            workout_type="strength",
            difficulty_level="intermediate",
            duration=30.0,
            category="strength",
            is_public=True
        )
        
        session.add(workout)
        session.commit()
        # Refresh the instance to ensure it's bound to the session
        session.refresh(workout)
        
        return workout

@pytest.fixture
def test_assignment(app, session, auth_headers, test_workout):
    """Create a test workout assignment"""
    print("######################")
    with app.app_context():
        user = auth_headers['user']
        
        assignment = WorkoutAssignment(
            user_id=user.id,
            workout_id=test_workout.id
        )
        
        session.add(assignment)
        session.commit()
        # Refresh the instance to ensure it's bound to the session
        session.refresh(assignment)
        
        return assignment