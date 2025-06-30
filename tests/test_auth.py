import unittest
import json
from app import create_app, db
from app.models.user import User
from app.models.revoked_token import RevokedToken

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Create all database tables
        db.create_all()
        
        # Create a test client
        self.client = self.app.test_client()
        
        # Create a test user
        self.test_user = User(
            username='testuser',
            email='test@example.com',
            first_name='Test',
            last_name='User'
        )
        self.test_user.password = 'Password123!'
        
        db.session.add(self.test_user)
        db.session.commit()
    
    def tearDown(self):
        # Remove all database tables
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def register_user(self, username='newuser'):
        """Helper method to register a new user"""
        return self.client.post('/api/users/register', 
            json={
                'username': username,
                'email': f'{username}@example.com',
                'password': 'Password123!',
                'confirm_password': 'Password123!',
                'first_name': 'New',
                'last_name': 'User'
            }
        )
    
    def login(self, username='testuser', password='Password123!'):
        """Helper method to login"""
        return self.client.post('/api/auth/login', 
            json={
                'username': username,
                'password': password
            }
        )
    
    def test_login_success(self):
        """Test successful login"""
        response = self.login()
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', data)
        self.assertIn('refresh_token', data)
        self.assertIn('user', data)
        
    def test_login_failure_wrong_password(self):
        """Test login with wrong password"""
        response = self.login(password='wrong_password')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 401)
        self.assertIn('error', data)
    
    def test_login_failure_user_not_found(self):
        """Test login with non-existent user"""
        response = self.login(username='nonexistentuser')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 401)
        self.assertIn('error', data)
    
    def test_registration_returns_tokens(self):
        """Test that registration returns tokens"""
        response = self.register_user()
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 201)
        self.assertIn('access_token', data)
        self.assertIn('refresh_token', data)
        self.assertIn('user', data)
    
    def test_protected_endpoint_with_token(self):
        """Test accessing a protected endpoint with a valid token"""
        # First login to get a token
        login_response = self.login()
        login_data = json.loads(login_response.data)
        access_token = login_data['access_token']
        
        # Now access protected endpoint
        headers = {'Authorization': f'Bearer {access_token}'}
        response = self.client.get(f'/api/users/{self.test_user.id}', headers=headers)
        
        self.assertEqual(response.status_code, 200)
    
    def test_protected_endpoint_without_token(self):
        """Test accessing a protected endpoint without a token"""
        response = self.client.get(f'/api/users/{self.test_user.id}')
        
        self.assertEqual(response.status_code, 401)
    
    def test_refresh_token(self):
        """Test refreshing an access token"""
        # First login to get tokens
        login_response = self.login()
        login_data = json.loads(login_response.data)
        refresh_token = login_data['refresh_token']
        
        # Use the refresh token to get a new access token
        refresh_response = self.client.post('/api/auth/refresh', json={
            'refresh_token': refresh_token
        })
        refresh_data = json.loads(refresh_response.data)
        
        self.assertEqual(refresh_response.status_code, 200)
        self.assertIn('access_token', refresh_data)
        
        # Verify the new access token works
        headers = {'Authorization': f'Bearer {refresh_data["access_token"]}'}
        response = self.client.get(f'/api/users/{self.test_user.id}', headers=headers)
        
        self.assertEqual(response.status_code, 200)
    
    def test_logout(self):
        """Test token revocation on logout"""
        # First login to get a token
        login_response = self.login()
        login_data = json.loads(login_response.data)
        access_token = login_data['access_token']
        
        # Now logout
        headers = {'Authorization': f'Bearer {access_token}'}
        logout_response = self.client.post('/api/auth/logout', headers=headers)
        
        self.assertEqual(logout_response.status_code, 200)
        
        # Try to access protected endpoint with the same token
        response = self.client.get(f'/api/users/{self.test_user.id}', headers=headers)
        
        # Token should be revoked
        self.assertEqual(response.status_code, 401)

if __name__ == '__main__':
    unittest.main()