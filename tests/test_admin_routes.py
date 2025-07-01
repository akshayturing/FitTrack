# # tests/test_admin_routes.py
# import unittest
# import json
# from app import create_app, db
# from app.models.user import User
# from app.models.exercise import Exercise, ExerciseType
# from app.models.workout import Workout, WorkoutExercise
# from datetime import datetime

# class AdminRoutesTestCase(unittest.TestCase):
#     """Test case for the admin routes."""
    
#     def setUp(self):
#         """Set up test client and test database."""
#         self.app = create_app('testing')
#         self.app.config['ADMIN_API_KEY'] = 'test-admin-key'
#         self.client = self.app.test_client()
#         self.admin_headers = {'X-API-Key': 'test-admin-key'}
        
#         # Create the test database
#         with self.app.app_context():
#             db.create_all()
#             self.setupTestData()
    
#     def tearDown(self):
#         """Clean up after test."""
#         with self.app.app_context():
#             db.session.remove()
#             db.drop_all()
    
#     def setupTestData(self):
#         """Set up test data in the database."""
#         # Create a test user
#         user = User(username='testuser', email='test@example.com')
#         user.password = 'Password123!'  # This should use your password setting mechanism
#         db.session.add(user)
#         db.session.commit()
#         self.test_user_id = user.id
        
#         # Create a test exercise
#         exercise = Exercise(
#             name='Test Exercise',
#             type=ExerciseType.STRENGTH,
#             description='Exercise description',
#             default_reps=10,
#             default_sets=3,
#             target_muscles='Test muscles',
#             instructions='Test instructions'
#         )
#         db.session.add(exercise)
#         db.session.commit()
#         self.test_exercise_id = exercise.id
        
#         # Create another test exercise
#         exercise2 = Exercise(
#             name='Test Exercise 2',
#             type=ExerciseType.CARDIO,
#             default_reps=15,
#             default_sets=4
#         )
#         db.session.add(exercise2)
#         db.session.commit()
#         self.test_exercise_id2 = exercise2.id
        
#         # Create a test workout
#         workout = Workout(
#             name='Test Workout',
#             description='Workout description',
#             user_id=self.test_user_id,
#             workout_type='strength',
#             duration=30
#         )
#         db.session.add(workout)
#         db.session.commit()
#         self.test_workout_id = workout.id
        
#         # Add exercises to the workout
#         workout_exercise1 = WorkoutExercise(
#             workout_id=self.test_workout_id,
#             exercise_id=self.test_exercise_id,
#             position=1,
#             custom_sets=4,
#             custom_reps=12,
#             notes='Test notes'
#         )
#         db.session.add(workout_exercise1)
#         db.session.commit()
    
#     # ============ Exercise CRUD Tests ============
    
#     def test_get_exercises(self):
#         """Test getting list of exercises."""
#         response = self.client.get('/admin/exercises', headers=self.admin_headers)
#         self.assertEqual(response.status_code, 200)
#         data = json.loads(response.data)
#         self.assertEqual(data['status'], 'success')
#         self.assertEqual(data['count'], 2)
#         self.assertEqual(len(data['data']), 2)
        
#     def test_get_exercises_unauthorized(self):
#         """Test getting exercises without API key."""
#         response = self.client.get('/admin/exercises')
#         self.assertEqual(response.status_code, 401)
        
#     def test_get_exercises_invalid_key(self):
#         """Test getting exercises with invalid API key."""
#         response = self.client.get('/admin/exercises', headers={'X-API-Key': 'invalid-key'})
#         self.assertEqual(response.status_code, 403)
        
#     def test_get_single_exercise(self):
#         """Test getting a single exercise."""
#         response = self.client.get(f'/admin/exercises/{self.test_exercise_id}', headers=self.admin_headers)
#         self.assertEqual(response.status_code, 200)
#         data = json.loads(response.data)
#         self.assertEqual(data['status'], 'success')
#         self.assertEqual(data['data']['name'], 'Test Exercise')
        
#     def test_get_nonexistent_exercise(self):
#         """Test getting a non-existent exercise."""
#         response = self.client.get('/admin/exercises/9999', headers=self.admin_headers)
#         self.assertEqual(response.status_code, 404)
        
#     def test_create_exercise(self):
#         """Test creating a new exercise."""
#         exercise_data = {
#             'name': 'New Exercise',
#             'type': 'strength',
#             'description': 'New description',
#             'default_reps': 12,
#             'default_sets': 3,
#             'target_muscles': 'New muscles',
#             'instructions': 'New instructions'
#         }
#         response = self.client.post('/admin/exercises', 
#                                     data=json.dumps(exercise_data),
#                                     content_type='application/json',
#                                     headers=self.admin_headers)
#         self.assertEqual(response.status_code, 201)
#         data = json.loads(response.data)
#         self.assertEqual(data['status'], 'success')
#         self.assertEqual(data['data']['name'], 'New Exercise')
        
#         # Verify exercise was created
#         with self.app.app_context():
#             exercise = Exercise.query.filter_by(name='New Exercise').first()
#             self.assertIsNotNone(exercise)
            
#     def test_create_exercise_missing_required(self):
#         """Test creating an exercise with missing required fields."""
#         exercise_data = {
#             'description': 'Missing required fields'
#         }
#         response = self.client.post('/admin/exercises', 
#                                     data=json.dumps(exercise_data),
#                                     content_type='application/json',
#                                     headers=self.admin_headers)
#         self.assertEqual(response.status_code, 400)
        
#     def test_create_exercise_invalid_type(self):
#         """Test creating an exercise with invalid type."""
#         exercise_data = {
#             'name': 'Invalid Type Exercise',
#             'type': 'invalid_type'
#         }
#         response = self.client.post('/admin/exercises', 
#                                     data=json.dumps(exercise_data),
#                                     content_type='application/json',
#                                     headers=self.admin_headers)
#         self.assertEqual(response.status_code, 400)
        
#     def test_create_duplicate_exercise(self):
#         """Test creating an exercise with duplicate name."""
#         exercise_data = {
#             'name': 'Test Exercise',  # Same name as existing exercise
#             'type': 'strength'
#         }
#         response = self.client.post('/admin/exercises', 
#                                     data=json.dumps(exercise_data),
#                                     content_type='application/json',
#                                     headers=self.admin_headers)
#         self.assertEqual(response.status_code, 409)
        
#     def test_update_exercise(self):
#         """Test updating an exercise."""
#         exercise_data = {
#             'name': 'Updated Exercise',
#             'description': 'Updated description'
#         }
#         response = self.client.put(f'/admin/exercises/{self.test_exercise_id}', 
#                                    data=json.dumps(exercise_data),
#                                    content_type='application/json',
#                                    headers=self.admin_headers)
#         self.assertEqual(response.status_code, 200)
#         data = json.loads(response.data)
#         self.assertEqual(data['status'], 'success')
#         self.assertEqual(data['data']['name'], 'Updated Exercise')
#         self.assertEqual(data['data']['description'], 'Updated description')
        
#         # Verify exercise was updated
#         with self.app.app_context():
#             exercise = Exercise.query.get(self.test_exercise_id)
#             self.assertEqual(exercise.name, 'Updated Exercise')
            
#     def test_update_nonexistent_exercise(self):
#         """Test updating a non-existent exercise."""
#         exercise_data = {
#             'name': 'This Should Fail'
#         }
#         response = self.client.put('/admin/exercises/9999', 
#                                    data=json.dumps(exercise_data),
#                                    content_type='application/json',
#                                    headers=self.admin_headers)
#         self.assertEqual(response.status_code, 404)
        
#     def test_delete_exercise(self):
#         """Test deleting an exercise."""
#         response = self.client.delete(f'/admin/exercises/{self.test_exercise_id2}', 
#                                      headers=self.admin_headers)
#         self.assertEqual(response.status_code, 200)
#         data = json.loads(response.data)
#         self.assertEqual(data['status'], 'success')
        
#         # Verify exercise was deleted
#         with self.app.app_context():
#             exercise = Exercise.query.get(self.test_exercise_id2)
#             self.assertIsNone(exercise)
            
#     def test_delete_nonexistent_exercise(self):
#         """Test deleting a non-existent exercise."""
#         response = self.client.delete('/admin/exercises/9999', 
#                                      headers=self.admin_headers)
#         self.assertEqual(response.status_code, 404)
    
#     # ============ Workout CRUD Tests ============
    
#     def test_get_workouts(self):
#         """Test getting list of workouts."""
#         response = self.client.get('/admin/workouts', headers=self.admin_headers)
#         self.assertEqual(response.status_code, 200)
#         data = json.loads(response.data)
#         self.assertEqual(data['status'], 'success')
#         self.assertEqual(data['count'], 1)
#         self.assertEqual(len(data['data']), 1)
        
#     def test_get_workouts_by_user(self):
#         """Test getting workouts filtered by user."""
#         response = self.client.get(f'/admin/workouts?user_id={self.test_user_id}', 
#                                   headers=self.admin_headers)
#         self.assertEqual(response.status_code, 200)
#         data = json.loads(response.data)
#         self.assertEqual(data['status'], 'success')
#         self.assertEqual(data['count'], 1)
        
#     def test_get_single_workout(self):
#         """Test getting a single workout."""
#         response = self.client.get(f'/admin/workouts/{self.test_workout_id}', 
#                                   headers=self.admin_headers)
#         self.assertEqual(response.status_code, 200)
#         data = json.loads(response.data)
#         self.assertEqual(data['status'], 'success')
#         self.assertEqual(data['data']['name'], 'Test Workout')
#         self.assertEqual(len(data['data']['exercises']), 1)
        
#     def test_get_nonexistent_workout(self):
#         """Test getting a non-existent workout."""
#         response = self.client.get('/admin/workouts/9999', headers=self.admin_headers)
#         self.assertEqual(response.status_code, 404)
        
#     def test_create_workout(self):
#         """Test creating a new workout with exercises."""
#         workout_data = {
#             'name': 'New Workout',
#             'description': 'New workout description',
#             'user_id': self.test_user_id,
#             'workout_type': 'cardio',
#             'duration': 45,
#             'exercises': [
#                 {
#                     'exercise_id': self.test_exercise_id,
#                     'custom_sets': 5,
#                     'custom_reps': 15,
#                     'notes': 'Exercise 1 notes'
#                 },
#                 {
#                     'exercise_id': self.test_exercise_id2,
#                     'custom_sets': 3,
#                     'custom_reps': 20,
#                     'notes': 'Exercise 2 notes'
#                 }
#             ]
#         }
#         response = self.client.post('/admin/workouts', 
#                                    data=json.dumps(workout_data),
#                                    content_type='application/json',
#                                    headers=self.admin_headers)
#         self.assertEqual(response.status_code, 201)
#         data = json.loads(response.data)
#         self.assertEqual(data['status'], 'success')
#         self.assertEqual(data['data']['name'], 'New Workout')
#         self.assertEqual(len(data['data']['exercises']), 2)
        
#         # Verify workout was created
#         with self.app.app_context():
#             workout = Workout.query.filter_by(name='New Workout').first()
#             self.assertIsNotNone(workout)
#             self.assertEqual(len(workout.workout_exercises), 2)
            
#     def test_create_workout_missing_required(self):
#         """Test creating a workout with missing required fields."""
#         workout_data = {
#             'description': 'Missing required fields'
#         }
#         response = self.client.post('/admin/workouts', 
#                                    data=json.dumps(workout_data),
#                                    content_type='application/json',
#                                    headers=self.admin_headers)
#         self.assertEqual(response.status_code, 400)
        
#     def test_create_workout_nonexistent_user(self):
#         """Test creating a workout for a non-existent user."""
#         workout_data = {
#             'name': 'Invalid User Workout',
#             'user_id': 9999
#         }
#         response = self.client.post('/admin/workouts', 
#                                    data=json.dumps(workout_data),
#                                    content_type='application/json',
#                                    headers=self.admin_headers)
#         self.assertEqual(response.status_code, 404)
        
#     def test_create_workout_invalid_exercise(self):
#         """Test creating a workout with an invalid exercise."""
#         workout_data = {
#             'name': 'Invalid Exercise Workout',
#             'user_id': self.test_user_id,
#             'exercises': [
#                 {
#                     'exercise_id': 9999  # Non-existent exercise
#                 }
#             ]
#         }
#         response = self.client.post('/admin/workouts', 
#                                    data=json.dumps(workout_data),
#                                    content_type='application/json',
#                                    headers=self.admin_headers)
#         self.assertEqual(response.status_code, 400)
#         data = json.loads(response.data)
#         self.assertTrue('errors' in data)
        
#     def test_update_workout(self):
#         """Test updating a workout."""
#         workout_data = {
#             'name': 'Updated Workout',
#             'description': 'Updated description',
#             'exercises': [
#                 {
#                     'exercise_id': self.test_exercise_id,
#                     'custom_sets': 6,
#                     'custom_reps': 10,
#                     'notes': 'Updated notes'
#                 }
#             ]
#         }
#         response = self.client.put(f'/admin/workouts/{self.test_workout_id}', 
#                                   data=json.dumps(workout_data),
#                                   content_type='application/json',
#                                   headers=self.admin_headers)
#         self.assertEqual(response.status_code, 200)
#         data = json.loads(response.data)
#         self.assertEqual(data['status'], 'success')
#         self.assertEqual(data['data']['name'], 'Updated Workout')
#         self.assertEqual(data['data']['description'], 'Updated description')
        
#         # Verify workout was updated
#         with self.app.app_context():
#             workout = Workout.query.get(self.test_workout_id)
#             self.assertEqual(workout.name, 'Updated Workout')
#             self.assertEqual(len(workout.workout_exercises), 1)
#             self.assertEqual(workout.workout_exercises[0].custom_sets, 6)
            
#     def test_update_nonexistent_workout(self):
#         """Test updating a non-existent workout."""
#         workout_data = {
#             'name': 'This Should Fail'
#         }
#         response = self.client.put('/admin/workouts/9999', 
#                                   data=json.dumps(workout_data),
#                                   content_type='application/json',
#                                   headers=self.admin_headers)
#         self.assertEqual(response.status_code, 404)
        
#     def test_delete_workout(self):
#         """Test deleting a workout."""
#         # First create a workout to delete
#         with self.app.app_context():
#             workout = Workout(
#                 name='Workout to Delete',
#                 user_id=self.test_user_id
#             )
#             db.session.add(workout)
#             db.session.commit()
#             workout_id = workout.id
        
#         response = self.client.delete(f'/admin/workouts/{workout_id}', 
#                                      headers=self.admin_headers)
#         self.assertEqual(response.status_code, 200)
#         data = json.loads(response.data)
#         self.assertEqual(data['status'], 'success')
        
#         # Verify workout was deleted
#         with self.app.app_context():
#             workout = Workout.query.get(workout_id)
#             self.assertIsNone(workout)
            
#     def test_delete_nonexistent_workout(self):
#         """Test deleting a non-existent workout."""
#         response = self.client.delete('/admin/workouts/9999', 
#                                      headers=self.admin_headers)
#         self.assertEqual(response.status_code, 404)
    
#     # ============ Workout Exercise Management Tests ============
    
#     def test_add_exercise_to_workout(self):
#         """Test adding an exercise to a workout."""
#         exercise_data = {
#             'exercise_id': self.test_exercise_id2,
#             'custom_sets': 5,
#             'custom_reps': 15,
#             'notes': 'Added exercise'
#         }
#         response = self.client.post(f'/admin/workouts/{self.test_workout_id}/exercises', 
#                                    data=json.dumps(exercise_data),
#                                    content_type='application/json',
#                                    headers=self.admin_headers)
#         self.assertEqual(response.status_code, 201)
#         data = json.loads(response.data)
#         self.assertEqual(data['status'], 'success')
        
#         # Check that there are now 2 exercises
#         self.assertEqual(len(data['data']['exercises']), 2)
        
#         # Verify exercise was added
#         with self.app.app_context():
#             workout = Workout.query.get(self.test_workout_id)
#             self.assertEqual(len(workout.workout_exercises), 2)
            
#     def test_add_exercise_to_nonexistent_workout(self):
#         """Test adding an exercise to a non-existent workout."""
#         exercise_data = {
#             'exercise_id': self.test_exercise_id
#         }
#         response = self.client.post('/admin/workouts/9999/exercises', 
#                                    data=json.dumps(exercise_data),
#                                    content_type='application/json',
#                                    headers=self.admin_headers)
#         self.assertEqual(response.status_code, 404)
        
#     def test_add_nonexistent_exercise_to_workout(self):
#         """Test adding a non-existent exercise to a workout."""
#         exercise_data = {
#             'exercise_id': 9999
#         }
#         response = self.client.post(f'/admin/workouts/{self.test_workout_id}/exercises', 
#                                    data=json.dumps(exercise_data),
#                                    content_type='application/json',
#                                    headers=self.admin_headers)
#         self.assertEqual(response.status_code, 404)
        
#     def test_remove_exercise_from_workout(self):
#         """Test removing an exercise from a workout."""
#         # First add a second exercise to the workout
#         with self.app.app_context():
#             workout_exercise = WorkoutExercise(
#                 workout_id=self.test_workout_id,
#                 exercise_id=self.test_exercise_id2,
#                 position=2
#             )
#             db.session.add(workout_exercise)
#             db.session.commit()
        
#         # Now delete the first exercise
#         response = self.client.delete(f'/admin/workouts/{self.test_workout_id}/exercises/{self.test_exercise_id}', 
#                                      headers=self.admin_headers)
#         self.assertEqual(response.status_code, 200)
#         data = json.loads(response.data)
#         self.assertEqual(data['status'], 'success')
        
#         # Check that there's only 1 exercise left
#         self.assertEqual(len(data['data']['exercises']), 1)
        
#         # Verify that positions were reordered
#         self.assertEqual(data['data']['exercises'][0]['position'], 1)
        
#     def test_remove_nonexistent_exercise_from_workout(self):
#         """Test removing a non-existent exercise from a workout."""
#         response = self.client.delete(f'/admin/workouts/{self.test_workout_id}/exercises/9999', 
#                                      headers=self.admin_headers)
#         self.assertEqual(response.status_code, 404)
        
#     def test_reorder_workout_exercises(self):
#         """Test reordering exercises in a workout."""
#         # First add a second exercise to the workout
#         with self.app.app_context():
#             workout_exercise = WorkoutExercise(
#                 workout_id=self.test_workout_id,
#                 exercise_id=self.test_exercise_id2,
#                 position=2
#             )
#             db.session.add(workout_exercise)
#             db.session.commit()
        
#         # Now reorder the exercises
#         reorder_data = {
#             'exercise_order': [self.test_exercise_id2, self.test_exercise_id]  # Reverse order
#         }
#         response = self.client.put(f'/admin/workouts/{self.test_workout_id}/exercises/reorder', 
#                                   data=json.dumps(reorder_data),
#                                   content_type='application/json',
#                                   headers=self.admin_headers)
#         self.assertEqual(response.status_code, 200)
#         data = json.loads(response.data)
#         self.assertEqual(data['status'], 'success')
        
#         # Check that exercises are in the new order
#         self.assertEqual(data['data']['exercises'][0]['exercise_id'], self.test_exercise_id2)
#         self.assertEqual(data['data']['exercises'][0]['position'], 1)
#         self.assertEqual(data['data']['exercises'][1]['exercise_id'], self.test_exercise_id)
#         self.assertEqual(data['data']['exercises'][1]['position'], 2)
        
#     def test_reorder_with_incomplete_list(self):
#         """Test reordering with an incomplete list of exercises."""
#         # First add a second exercise to the workout
#         with self.app.app_context():
#             workout_exercise = WorkoutExercise(
#                 workout_id=self.test_workout_id,
#                 exercise_id=self.test_exercise_id2,
#                 position=2
#             )
#             db.session.add(workout_exercise)
#             db.session.commit()
        
#         # Now try to reorder with incomplete list
#         reorder_data = {
#             'exercise_order': [self.test_exercise_id]  # Missing second exercise
#         }
#         response = self.client.put(f'/admin/workouts/{self.test_workout_id}/exercises/reorder', 
#                                   data=json.dumps(reorder_data),
#                                   content_type='application/json',
#                                   headers=self.admin_headers)
#         self.assertEqual(response.status_code, 400)
#         data = json.loads(response.data)
#         self.assertEqual(data['status'], 'error')
        
# if __name__ == '__main__':
#     unittest.main()
import json
import pytest
from datetime import datetime
from flask import url_for
from app import create_app, db
from app.models.user import User
from app.models.exercise import Exercise, ExerciseType
from app.models.workout import Workout
from app.models.workout_exercise import WorkoutExercise

# Test data
ADMIN_API_KEY = 'admin-secret-key'
TEST_USER_DATA = {
    'username': 'testuser',
    'email': 'test@example.com',
    'password': 'TestPassword123!'
}
TEST_EXERCISE_DATA = {
    'name': 'Test Exercise',
    'type': 'strength',
    'description': 'Test description',
    'default_reps': 10,
    'default_sets': 3,
    'target_muscles': 'Test muscles',
    'instructions': 'Test instructions'
}
TEST_WORKOUT_DATA = {
    'name': 'Test Workout',
    'description': 'Test workout description',
    'workout_type': 'strength',
    'duration': 60
}

@pytest.fixture
def app():
    """Create and configure a Flask app for testing"""
    app = create_app('testing')
    app.config['TESTING'] = True
    app.config['ADMIN_API_KEY'] = ADMIN_API_KEY
    
    # Create all tables
    with app.app_context():
        db.create_all()
        
        # Create a test user
        user = User(username=TEST_USER_DATA['username'], email=TEST_USER_DATA['email'])
        user.password = TEST_USER_DATA['password']
        db.session.add(user)
        db.session.commit()
        
        # Store the user id for later use in tests
        app.config['TEST_USER_ID'] = user.id
    
    yield app
    
    # Clean up
    with app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """A test client for the app"""
    return app.test_client()

@pytest.fixture
def auth_headers():
    """Headers with admin API key"""
    return {'X-API-Key': ADMIN_API_KEY, 'Content-Type': 'application/json'}

@pytest.fixture
def created_exercise(app, client, auth_headers):
    """Create a test exercise and return it"""
    with app.app_context():
        response = client.post(
            '/admin/exercises',
            data=json.dumps(TEST_EXERCISE_DATA),
            headers=auth_headers
        )
        return json.loads(response.data)['data']

@pytest.fixture
def created_workout(app, client, auth_headers, created_exercise):
    """Create a test workout with an exercise and return it"""
    with app.app_context():
        # Prepare workout data with a test user and exercise
        workout_data = TEST_WORKOUT_DATA.copy()
        workout_data['user_id'] = app.config['TEST_USER_ID']
        workout_data['exercises'] = [
            {
                'exercise_id': created_exercise['id'],
                'custom_sets': 4,
                'custom_reps': 15
            }
        ]
        
        response = client.post(
            '/admin/workouts',
            data=json.dumps(workout_data),
            headers=auth_headers
        )
        return json.loads(response.data)['data']

#########################################
# Tests for Exercise CRUD Endpoints
#########################################

def test_create_exercise(client, auth_headers):
    """Test creating a new exercise"""
    response = client.post(
        '/admin/exercises',
        data=json.dumps(TEST_EXERCISE_DATA),
        headers=auth_headers
    )
    data = json.loads(response.data)
    
    assert response.status_code == 201
    assert data['status'] == 'success'
    assert data['data']['name'] == TEST_EXERCISE_DATA['name']
    assert data['data']['type'] == TEST_EXERCISE_DATA['type']
    assert 'id' in data['data']

def test_create_exercise_missing_fields(client, auth_headers):
    """Test creating an exercise with missing required fields"""
    # Missing name field
    incomplete_data = {
        'type': 'strength',
        'description': 'Test description'
    }
    
    response = client.post(
        '/admin/exercises',
        data=json.dumps(incomplete_data),
        headers=auth_headers
    )
    data = json.loads(response.data)
    
    assert response.status_code == 400
    assert data['status'] == 'error'
    assert 'Missing required field' in data['message']

def test_create_exercise_invalid_type(client, auth_headers):
    """Test creating an exercise with invalid type"""
    invalid_data = TEST_EXERCISE_DATA.copy()
    invalid_data['type'] = 'invalid_type'
    
    response = client.post(
        '/admin/exercises',
        data=json.dumps(invalid_data),
        headers=auth_headers
    )
    data = json.loads(response.data)
    
    assert response.status_code == 400
    assert data['status'] == 'error'
    assert 'Invalid exercise type' in data['message']

def test_create_duplicate_exercise(client, auth_headers, created_exercise):
    """Test creating an exercise with a duplicate name"""
    duplicate_data = TEST_EXERCISE_DATA.copy()
    
    response = client.post(
        '/admin/exercises',
        data=json.dumps(duplicate_data),
        headers=auth_headers
    )
    data = json.loads(response.data)
    
    assert response.status_code == 409
    assert data['status'] == 'error'
    assert 'already exists' in data['message']

def test_get_all_exercises(client, auth_headers, created_exercise):
    """Test getting all exercises"""
    response = client.get(
        '/admin/exercises',
        headers=auth_headers
    )
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data['status'] == 'success'
    assert isinstance(data['data'], list)
    assert len(data['data']) > 0
    assert data['data'][0]['name'] == TEST_EXERCISE_DATA['name']

def test_filter_exercises_by_type(client, auth_headers, created_exercise):
    """Test filtering exercises by type"""
    # First, create an exercise with a different type
    cardio_exercise = TEST_EXERCISE_DATA.copy()
    cardio_exercise['name'] = 'Cardio Exercise'
    cardio_exercise['type'] = 'cardio'
    
    client.post(
        '/admin/exercises',
        data=json.dumps(cardio_exercise),
        headers=auth_headers
    )
    
    # Test filter
    response = client.get(
        '/admin/exercises?type=strength',
        headers=auth_headers
    )
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data['status'] == 'success'
    assert all(ex['type'] == 'strength' for ex in data['data'])
    
    # Test other type
    response = client.get(
        '/admin/exercises?type=cardio',
        headers=auth_headers
    )
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data['status'] == 'success'
    assert all(ex['type'] == 'cardio' for ex in data['data'])

def test_get_exercise_by_id(client, auth_headers, created_exercise):
    """Test getting a specific exercise by ID"""
    response = client.get(
        f'/admin/exercises/{created_exercise["id"]}',
        headers=auth_headers
    )
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data['status'] == 'success'
    assert data['data']['id'] == created_exercise['id']
    assert data['data']['name'] == TEST_EXERCISE_DATA['name']

def test_get_nonexistent_exercise(client, auth_headers):
    """Test getting a nonexistent exercise"""
    response = client.get(
        '/admin/exercises/9999',
        headers=auth_headers
    )
    data = json.loads(response.data)
    
    assert response.status_code == 404
    assert data['status'] == 'error'
    assert 'not found' in data['message']

def test_update_exercise(client, auth_headers, created_exercise):
    """Test updating an exercise"""
    update_data = {
        'name': 'Updated Exercise Name',
        'description': 'Updated description',
        'default_reps': 12
    }
    
    response = client.put(
        f'/admin/exercises/{created_exercise["id"]}',
        data=json.dumps(update_data),
        headers=auth_headers
    )
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data['status'] == 'success'
    assert data['data']['name'] == update_data['name']
    assert data['data']['description'] == update_data['description']
    assert data['data']['default_reps'] == update_data['default_reps']
    assert data['data']['default_sets'] == TEST_EXERCISE_DATA['default_sets']  # Unchanged

def test_update_exercise_type(client, auth_headers, created_exercise):
    """Test updating an exercise type"""
    update_data = {
        'type': 'cardio'
    }
    
    response = client.put(
        f'/admin/exercises/{created_exercise["id"]}',
        data=json.dumps(update_data),
        headers=auth_headers
    )
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data['status'] == 'success'
    assert data['data']['type'] == 'cardio'

def test_update_exercise_invalid_type(client, auth_headers, created_exercise):
    """Test updating an exercise with an invalid type"""
    update_data = {
        'type': 'invalid_type'
    }
    
    response = client.put(
        f'/admin/exercises/{created_exercise["id"]}',
        data=json.dumps(update_data),
        headers=auth_headers
    )
    data = json.loads(response.data)
    
    assert response.status_code == 400
    assert data['status'] == 'error'
    assert 'Invalid exercise type' in data['message']

def test_delete_exercise(client, auth_headers, created_exercise):
    """Test deleting an exercise"""
    response = client.delete(
        f'/admin/exercises/{created_exercise["id"]}',
        headers=auth_headers
    )
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data['status'] == 'success'
    
    # Verify it's deleted
    response = client.get(
        f'/admin/exercises/{created_exercise["id"]}',
        headers=auth_headers
    )
    
    assert response.status_code == 404

def test_delete_nonexistent_exercise(client, auth_headers):
    """Test deleting a nonexistent exercise"""
    response = client.delete(
        '/admin/exercises/9999',
        headers=auth_headers
    )
    data = json.loads(response.data)
    
    assert response.status_code == 404
    assert data['status'] == 'error'
    assert 'not found' in data['message']

def test_unauthorized_access(client):
    """Test accessing endpoints without API key"""
    response = client.get('/admin/exercises')
    data = json.loads(response.data)
    
    assert response.status_code == 401
    assert data['status'] == 'error'
    assert 'API key is missing' in data['message']

def test_invalid_api_key(client):
    """Test accessing endpoints with invalid API key"""
    headers = {'X-API-Key': 'invalid-key', 'Content-Type': 'application/json'}
    
    response = client.get('/admin/exercises', headers=headers)
    data = json.loads(response.data)
    
    assert response.status_code == 403
    assert data['status'] == 'error'
    assert 'Invalid API key' in data['message']

#########################################
# Tests for Workout CRUD Endpoints
#########################################

def test_create_workout(app, client, auth_headers, created_exercise):
    """Test creating a new workout with exercises"""
    # Prepare workout data
    workout_data = TEST_WORKOUT_DATA.copy()
    workout_data['user_id'] = app.config['TEST_USER_ID']
    workout_data['exercises'] = [
        {
            'exercise_id': created_exercise['id'],
            'custom_sets': 4,
            'custom_reps': 15,
            'notes': 'Test notes'
        }
    ]
    
    response = client.post(
        '/admin/workouts',
        data=json.dumps(workout_data),
        headers=auth_headers
    )
    data = json.loads(response.data)
    
    assert response.status_code == 201
    assert data['status'] == 'success'
    assert data['data']['name'] == workout_data['name']
    assert data['data']['user_id'] == workout_data['user_id']
    assert len(data['data']['exercises']) == 1
    assert data['data']['exercises'][0]['exercise_id'] == created_exercise['id']
    assert data['data']['exercises'][0]['sets'] == 4  # Custom sets
    assert data['data']['exercises'][0]['reps'] == 15  # Custom reps
    assert data['data']['exercises'][0]['notes'] == 'Test notes'

def test_create_workout_missing_fields(client, auth_headers):
    """Test creating a workout with missing required fields"""
    # Missing name field
    incomplete_data = {
        'description': 'Test description'
    }
    
    response = client.post(
        '/admin/workouts',
        data=json.dumps(incomplete_data),
        headers=auth_headers
    )
    data = json.loads(response.data)
    
    assert response.status_code == 400
    assert data['status'] == 'error'
    assert 'Missing required field' in data['message']

def test_create_workout_invalid_user(client, auth_headers):
    """Test creating a workout with invalid user_id"""
    invalid_data = TEST_WORKOUT_DATA.copy()
    invalid_data['user_id'] = 9999  # Non-existent user
    
    response = client.post(
        '/admin/workouts',
        data=json.dumps(invalid_data),
        headers=auth_headers
    )
    data = json.loads(response.data)
    
    assert response.status_code == 404
    assert data['status'] == 'error'
    assert 'User with id' in data['message']
    assert 'not found' in data['message']

def test_create_workout_invalid_exercise(app, client, auth_headers):
    """Test creating a workout with invalid exercise"""
    workout_data = TEST_WORKOUT_DATA.copy()
    workout_data['user_id'] = app.config['TEST_USER_ID']
    workout_data['exercises'] = [
        {
            'exercise_id': 9999,  # Non-existent exercise
            'custom_sets': 4,
            'custom_reps': 15
        }
    ]
    
    response = client.post(
        '/admin/workouts',
        data=json.dumps(workout_data),
        headers=auth_headers
    )
    data = json.loads(response.data)
    
    assert response.status_code == 400
    assert data['status'] == 'error'
    assert 'Invalid exercises in request' in data['message']
    assert 'not found' in data['errors'][0]['error']

def test_get_all_workouts(client, auth_headers, created_workout):
    """Test getting all workouts"""
    response = client.get(
        '/admin/workouts',
        headers=auth_headers
    )
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data['status'] == 'success'
    assert isinstance(data['data'], list)
    assert len(data['data']) > 0
    assert data['data'][0]['name'] == TEST_WORKOUT_DATA['name']
    assert 'exercises' in data['data'][0]
    assert len(data['data'][0]['exercises']) > 0

def test_filter_workouts_by_user(app, client, auth_headers, created_workout):
    """Test filtering workouts by user"""
    response = client.get(
        f'/admin/workouts?user_id={app.config["TEST_USER_ID"]}',
        headers=auth_headers
    )
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data['status'] == 'success'
    assert all(workout['user_id'] == app.config['TEST_USER_ID'] for workout in data['data'])

def test_get_workout_by_id(client, auth_headers, created_workout):
    """Test getting a specific workout by ID"""
    response = client.get(
        f'/admin/workouts/{created_workout["id"]}',
        headers=auth_headers
    )
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data['status'] == 'success'
    assert data['data']['id'] == created_workout['id']
    assert data['data']['name'] == TEST_WORKOUT_DATA['name']
    assert 'exercises' in data['data']
    assert len(data['data']['exercises']) > 0

def test_get_nonexistent_workout(client, auth_headers):
    """Test getting a nonexistent workout"""
    response = client.get(
        '/admin/workouts/9999',
        headers=auth_headers
    )
    data = json.loads(response.data)
    
    assert response.status_code == 404
    assert data['status'] == 'error'
    assert 'not found' in data['message']

def test_update_workout(client, auth_headers, created_workout):
    """Test updating a workout's basic information"""
    update_data = {
        'name': 'Updated Workout Name',
        'description': 'Updated description',
        'duration': 90
    }
    
    response = client.put(
        f'/admin/workouts/{created_workout["id"]}',
        data=json.dumps(update_data),
        headers=auth_headers
    )
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data['status'] == 'success'
    assert data['data']['name'] == update_data['name']
    assert data['data']['description'] == update_data['description']
    assert data['data']['duration'] == update_data['duration']

def test_update_workout_exercises(app, client, auth_headers, created_workout, created_exercise):
    """Test updating a workout's exercises"""
    # Create a second exercise for our test
    second_exercise = TEST_EXERCISE_DATA.copy()
    second_exercise['name'] = 'Second Test Exercise'
    
    response = client.post(
        '/admin/exercises',
        data=json.dumps(second_exercise),
        headers=auth_headers
    )
    second_exercise_data = json.loads(response.data)['data']
    
    # Update workout with new exercise list
    update_data = {
        'exercises': [
            {
                'exercise_id': created_exercise['id'],
                'custom_sets': 5,
                'custom_reps': 20,
                'notes': 'Updated notes'
            },
            {
                'exercise_id': second_exercise_data['id'],
                'custom_sets': 3,
                'custom_reps': 12,
                'notes': 'Second exercise notes'
            }
        ]
    }
    
    response = client.put(
        f'/admin/workouts/{created_workout["id"]}',
        data=json.dumps(update_data),
        headers=auth_headers
    )
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data['status'] == 'success'
    assert len(data['data']['exercises']) == 2
    assert data['data']['exercises'][0]['sets'] == 5  # Updated sets
    assert data['data']['exercises'][0]['notes'] == 'Updated notes'
    assert data['data']['exercises'][1]['exercise_id'] == second_exercise_data['id']

def test_update_workout_invalid_exercise(client, auth_headers, created_workout):
    """Test updating a workout with invalid exercise"""
    update_data = {
        'exercises': [
            {
                'exercise_id': 9999,  # Non-existent exercise
                'custom_sets': 5,
                'custom_reps': 20
            }
        ]
    }
    
    response = client.put(
        f'/admin/workouts/{created_workout["id"]}',
        data=json.dumps(update_data),
        headers=auth_headers
    )
    data = json.loads(response.data)
    
    assert response.status_code == 400
    assert data['status'] == 'error'
    assert 'Invalid exercises in request' in data['message']

def test_delete_workout(client, auth_headers, created_workout):
    """Test deleting a workout"""
    response = client.delete(
        f'/admin/workouts/{created_workout["id"]}',
        headers=auth_headers
    )
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data['status'] == 'success'
    
    # Verify it's deleted
    response = client.get(
        f'/admin/workouts/{created_workout["id"]}',
        headers=auth_headers
    )
    
    assert response.status_code == 404

def test_delete_nonexistent_workout(client, auth_headers):
    """Test deleting a nonexistent workout"""
    response = client.delete(
        '/admin/workouts/9999',
        headers=auth_headers
    )
    data = json.loads(response.data)
    
    assert response.status_code == 404
    assert data['status'] == 'error'
    assert 'not found' in data['message']

#########################################
# Tests for Workout Exercise Management
#########################################

def test_add_exercise_to_workout(client, auth_headers, created_workout, created_exercise):
    """Test adding an exercise to an existing workout"""
    # Create a second exercise for our test
    second_exercise = TEST_EXERCISE_DATA.copy()
    second_exercise['name'] = 'Second Test Exercise'
    
    response = client.post(
        '/admin/exercises',
        data=json.dumps(second_exercise),
        headers=auth_headers
    )
    second_exercise_data = json.loads(response.data)['data']
    
    # Add the exercise to the workout
    add_data = {
        'exercise_id': second_exercise_data['id'],
        'custom_sets': 4,
        'custom_reps': 12,
        'notes': 'Added exercise notes'
    }
    
    response = client.post(
        f'/admin/workouts/{created_workout["id"]}/exercises',
        data=json.dumps(add_data),
        headers=auth_headers
    )
    data = json.loads(response.data)
    
    assert response.status_code == 201
    assert data['status'] == 'success'
    assert len(data['data']['exercises']) == 2
    assert data['data']['exercises'][1]['exercise_id'] == second_exercise_data['id']
    assert data['data']['exercises'][1]['sets'] == 4
    assert data['data']['exercises'][1]['reps'] == 12
    assert data['data']['exercises'][1]['notes'] == 'Added exercise notes'

def test_add_exercise_with_position(client, auth_headers, created_workout, created_exercise):
    """Test adding an exercise to a specific position in the workout"""
    # Create a new exercise
    new_exercise = TEST_EXERCISE_DATA.copy()
    new_exercise['name'] = 'Position Test Exercise'
    
    response = client.post(
        '/admin/exercises',
        data=json.dumps(new_exercise),
        headers=auth_headers
    )
    new_exercise_data = json.loads(response.data)['data']
    
    # Add the exercise to the workout at position 1 (first)
    add_data = {
        'exercise_id': new_exercise_data['id'],
        'position': 1,
        'custom_sets': 3,
        'custom_reps': 15
    }
    
    response = client.post(
        f'/admin/workouts/{created_workout["id"]}/exercises',
        data=json.dumps(add_data),
        headers=auth_headers
    )
    data = json.loads(response.data)
    
    assert response.status_code == 201
    assert data['status'] == 'success'
    assert len(data['data']['exercises']) == 2
    # New exercise should be first
    assert data['data']['exercises'][0]['exercise_id'] == new_exercise_data['id']
    assert data['data']['exercises'][0]['position'] == 1
    # Original exercise should be shifted to position 2
    assert data['data']['exercises'][1]['exercise_id'] == created_exercise['id']
    assert data['data']['exercises'][1]['position'] == 2

def test_remove_exercise_from_workout(client, auth_headers, created_workout, created_exercise):
    """Test removing an exercise from a workout"""
    response = client.delete(
        f'/admin/workouts/{created_workout["id"]}/exercises/{created_exercise["id"]}',
        headers=auth_headers
    )
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data['status'] == 'success'
    assert len(data['data']['exercises']) == 0

def test_reorder_workout_exercises(client, auth_headers, created_workout, created_exercise):
    """Test reordering exercises in a workout"""
    # First, add another exercise
    second_exercise = TEST_EXERCISE_DATA.copy()
    second_exercise['name'] = 'Reorder Test Exercise'
    
    response = client.post(
        '/admin/exercises',
        data=json.dumps(second_exercise),
        headers=auth_headers
    )
    second_exercise_data = json.loads(response.data)['data']
    
    # Add the exercise to the workout
    add_data = {
        'exercise_id': second_exercise_data['id']
    }
    
    client.post(
        f'/admin/workouts/{created_workout["id"]}/exercises',
        data=json.dumps(add_data),
        headers=auth_headers
    )
    
    # Now reorder them (swap positions)
    reorder_data = {
        'exercise_order': [
            second_exercise_data['id'],
            created_exercise['id']
        ]
    }
    
    response = client.put(
        f'/admin/workouts/{created_workout["id"]}/exercises/reorder',
        data=json.dumps(reorder_data),
        headers=auth_headers
    )
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data['status'] == 'success'
    assert len(data['data']['exercises']) == 2
    # Exercises should be in the new order
    assert data['data']['exercises'][0]['exercise_id'] == second_exercise_data['id']
    assert data['data']['exercises'][0]['position'] == 1
    assert data['data']['exercises'][1]['exercise_id'] == created_exercise['id']
    assert data['data']['exercises'][1]['position'] == 2

def test_reorder_with_missing_exercise(client, auth_headers, created_workout, created_exercise):
    """Test reordering with a missing exercise"""
    # First add another exercise to the workout
    second_exercise = TEST_EXERCISE_DATA.copy()
    second_exercise['name'] = 'Reorder Missing Test Exercise'
    
    response = client.post(
        '/admin/exercises',
        data=json.dumps(second_exercise),
        headers=auth_headers
    )
    second_exercise_data = json.loads(response.data)['data']
    
    client.post(
        f'/admin/workouts/{created_workout["id"]}/exercises',
        data=json.dumps({'exercise_id': second_exercise_data['id']}),
        headers=auth_headers
    )
    
    # Attempt to reorder with a missing exercise
    reorder_data = {
        'exercise_order': [second_exercise_data['id']]  # Missing the first exercise
    }
    
    response = client.put(
        f'/admin/workouts/{created_workout["id"]}/exercises/reorder',
        data=json.dumps(reorder_data),
        headers=auth_headers
    )
    data = json.loads(response.data)
    
    assert response.status_code == 400
    assert data['status'] == 'error'
    assert 'All workout exercises must be included' in data['message']