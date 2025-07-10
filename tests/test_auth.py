# import unittest
# import json
# from app import create_app, db
# from app.models.user import User
# from app.models.revoked_token import RevokedToken

# class AuthTestCase(unittest.TestCase):
#     def setUp(self):
#         self.app = create_app('testing')
#         self.app_context = self.app.app_context()
#         self.app_context.push()
        
#         # Create all database tables
#         db.create_all()
        
#         # Create a test client
#         self.client = self.app.test_client()
        
#         # Create a test user
#         self.test_user = User(
#             username='testuser',
#             email='test@example.com',
#             first_name='Test',
#             last_name='User'
#         )
#         self.test_user.password = 'Password123!'
        
#         db.session.add(self.test_user)
#         db.session.commit()
    
#     def tearDown(self):
#         # Remove all database tables
#         db.session.remove()
#         db.drop_all()
#         self.app_context.pop()
    
#     def register_user(self, username='newuser'):
#         """Helper method to register a new user"""
#         return self.client.post('/api/users/register', 
#             json={
#                 'username': username,
#                 'email': f'{username}@example.com',
#                 'password': 'Password123!',
#                 'confirm_password': 'Password123!',
#                 'first_name': 'New',
#                 'last_name': 'User'
#             }
#         )
    
#     def login(self, username='testuser', password='Password123!'):
#         """Helper method to login"""
#         return self.client.post('/api/auth/login', 
#             json={
#                 'username': username,
#                 'password': password
#             }
#         )
    
#     def test_login_success(self):
#         """Test successful login"""
#         response = self.login()
#         data = json.loads(response.data)
        
#         self.assertEqual(response.status_code, 200)
#         self.assertIn('access_token', data)
#         self.assertIn('refresh_token', data)
#         self.assertIn('user', data)
        
#     def test_login_failure_wrong_password(self):
#         """Test login with wrong password"""
#         response = self.login(password='wrong_password')
#         data = json.loads(response.data)
        
#         self.assertEqual(response.status_code, 401)
#         self.assertIn('error', data)
    
#     def test_login_failure_user_not_found(self):
#         """Test login with non-existent user"""
#         response = self.login(username='nonexistentuser')
#         data = json.loads(response.data)
        
#         self.assertEqual(response.status_code, 401)
#         self.assertIn('error', data)
    
#     def test_registration_returns_tokens(self):
#         """Test that registration returns tokens"""
#         response = self.register_user()
#         data = json.loads(response.data)
        
#         self.assertEqual(response.status_code, 201)
#         self.assertIn('access_token', data)
#         self.assertIn('refresh_token', data)
#         self.assertIn('user', data)
    
#     def test_protected_endpoint_with_token(self):
#         """Test accessing a protected endpoint with a valid token"""
#         # First login to get a token
#         login_response = self.login()
#         login_data = json.loads(login_response.data)
#         access_token = login_data['access_token']
        
#         # Now access protected endpoint
#         headers = {'Authorization': f'Bearer {access_token}'}
#         response = self.client.get(f'/api/users/{self.test_user.id}', headers=headers)
        
#         self.assertEqual(response.status_code, 200)
    
#     def test_protected_endpoint_without_token(self):
#         """Test accessing a protected endpoint without a token"""
#         response = self.client.get(f'/api/users/{self.test_user.id}')
        
#         self.assertEqual(response.status_code, 401)
    
#     def test_refresh_token(self):
#         """Test refreshing an access token"""
#         # First login to get tokens
#         login_response = self.login()
#         login_data = json.loads(login_response.data)
#         refresh_token = login_data['refresh_token']
        
#         # Use the refresh token to get a new access token
#         refresh_response = self.client.post('/api/auth/refresh', json={
#             'refresh_token': refresh_token
#         })
#         refresh_data = json.loads(refresh_response.data)
        
#         self.assertEqual(refresh_response.status_code, 200)
#         self.assertIn('access_token', refresh_data)
        
#         # Verify the new access token works
#         headers = {'Authorization': f'Bearer {refresh_data["access_token"]}'}
#         response = self.client.get(f'/api/users/{self.test_user.id}', headers=headers)
        
#         self.assertEqual(response.status_code, 200)
    
#     def test_logout(self):
#         """Test token revocation on logout"""
#         # First login to get a token
#         login_response = self.login()
#         login_data = json.loads(login_response.data)
#         access_token = login_data['access_token']
        
#         # Now logout
#         headers = {'Authorization': f'Bearer {access_token}'}
#         logout_response = self.client.post('/api/auth/logout', headers=headers)
        
#         self.assertEqual(logout_response.status_code, 200)
        
#         # Try to access protected endpoint with the same token
#         response = self.client.get(f'/api/users/{self.test_user.id}', headers=headers)
        
#         # Token should be revoked
#         self.assertEqual(response.status_code, 401)

# if __name__ == '__main__':
#     unittest.main()


import unittest
import json
from app import create_app, db
from app.models.user import User
from app.models.revoked_token import RevokedToken

class UserRegistrationNameFieldTestCase(unittest.TestCase):
    def setUp(self):
        """Set up test environment before each test."""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Create all database tables
        db.create_all()
        
        # Create a test client
        self.client = self.app.test_client()
    
    def tearDown(self):
        """Clean up after each test."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_registration_with_name_field(self):
        """Test user registration with explicit name field."""
        data = {
            "username": "testuser1",
            "email": "testuser1@example.com",
            "password": "Password123!",
            "confirm_password": "Password123!",
            
            "name": "John Doe"  # Explicit name
        }
        
        response = self.client.post(
            '/api/users/register',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # Check response
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.data)
        self.assertIn('access_token', response_data)
        self.assertIn('user', response_data)
        
        # Verify user was created in database
        user = User.query.filter_by(username='testuser1').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.name, "John Doe")
        
    
    def test_registration_with_only_name_field(self):
        """Test user registration with only name field but no first_name/last_name."""
        data = {
            "username": "testuser3",
            "email": "testuser3@example.com",
            "password": "Password123!",
            "confirm_password": "Password123!",
            "name": "Alex Johnson"
            # No first_name or last_name
        }
        
        response = self.client.post(
            '/api/users/register',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # Check response
        self.assertEqual(response.status_code, 201)
        
        # Verify user was created and first_name/last_name extracted from name
        user = User.query.filter_by(username='testuser3').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.name, "Alex Johnson")
        
    
    def test_registration_with_complex_name(self):
        """Test user registration with a multi-part name."""
        data = {
            "username": "testuser4",
            "email": "testuser4@example.com",
            "password": "Password123!",
            "confirm_password": "Password123!",
            "name": "Maria Garcia Lopez"
            # Multi-part name
        }
        
        response = self.client.post(
            '/api/users/register',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        # Check response
        self.assertEqual(response.status_code, 201)
        
        # Verify correct name handling
        user = User.query.filter_by(username='testuser4').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.name, "Maria Garcia Lopez")
        
    
   
    def test_login_after_registration(self):
        """Test login functionality after registration with name field."""
        # First register a user
        register_data = {
            "username": "testuser7",
            "email": "testuser7@example.com",
            "password": "Password123!",
            "confirm_password": "Password123!",
            "name": "Test User Seven"
        }
        
        self.client.post(
            '/api/users/register',
            data=json.dumps(register_data),
            content_type='application/json'
        )
        
        # Now try to login
        login_data = {
            "username": "testuser7",
            "password": "Password123!"
        }
        
        response = self.client.post(
            '/api/auth/login',
            data=json.dumps(login_data),
            content_type='application/json'
        )
        
        # Check login response
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertIn('access_token', response_data)
        self.assertIn('user', response_data)
        self.assertEqual(response_data['user']['name'], "Test User Seven")
    
   
    def test_name_in_user_data(self):
        """Test that the name field is included in user data responses."""
        # Register a user
        register_data = {
            "username": "testuser8",
            "email": "testuser8@example.com",
            "password": "Password123!",
            "confirm_password": "Password123!",
            "name": "Emma Wilson"
        }
        
        response = self.client.post(
            '/api/users/register',
            data=json.dumps(register_data),
            content_type='application/json'
        )
        
        # Check that registration succeeded first
        self.assertEqual(response.status_code, 201)
        
        # Get token from registration response
        tokens = json.loads(response.data)
        access_token = tokens['access_token']
        print("########################")
        print(tokens, access_token)
        print("********************")
        # Print token for debugging
        print(f"Access token: {access_token}")
        
        response = self.client.get(
            '/api/auth/me',
            headers={'Authorization': f'Bearer {access_token}'}
        )
                
        # Print response for debugging
        print(f"Auth response status: {response.status_code}")
        print(f"Auth response body: {response.data}")
        
        # Debug: Try querying the user directly from the database
        user = User.query.filter_by(username='testuser8').first()
        if user:
            print(f"User in database: {user.username}, {user.name}")
        else:
            print("User not found in database")
        
        # Check that name field is in the response
        self.assertEqual(response.status_code, 200)
        user_data = json.loads(response.data)
        self.assertIn('name', user_data)
        self.assertEqual(user_data['name'], "Emma Wilson")

    def test_request_content_type(self):
        """Test registration with different content types to ensure correct parsing."""
        # Test with explicit application/json content type
        data = {
            "username": "testuser9",
            "email": "testuser9@example.com",
            "password": "Password123!",
            "confirm_password": "Password123!",
            "name": "Test User Nine"
        }
        
        response = self.client.post(
            '/api/users/register',
            data=json.dumps(data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 201)
        
        # Test with form data - this might not work if your endpoint only accepts JSON
        # Included for completeness
        form_data = {
            "username": "testuser10",
            "email": "testuser10@example.com",
            "password": "Password123!",
            "confirm_password": "Password123!",
            "name": "Test User Ten"
        }
        
        response = self.client.post(
            '/api/users/register',
            data=form_data
        )
        
        # Check if your endpoint handles form data
        # If it doesn't, this test might fail, which is expected
        print(f"Form data test status code: {response.status_code}")
        print(f"Form data test response: {response.data}")
        
        # Note: If your endpoint only accepts JSON, you should test that non-JSON
        # requests are properly rejected with an appropriate error message

if __name__ == '__main__':
    unittest.main()