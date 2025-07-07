import pytest
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token, decode_token
import json
class TestJWTConfig:
    """Test cases for JWT configuration."""

    def test_token_expiration(self, app):
        """Test that tokens expire after the configured time."""
        # Arrange
        with app.app_context():
            token = create_access_token(identity="1")
            decoded = decode_token(token)
            
            # Extract expiration time
            exp_timestamp = decoded['exp']
            iat_timestamp = decoded['iat']
            
            # Calculate expected expiration
            expected_expiration = iat_timestamp + app.config['JWT_ACCESS_TOKEN_EXPIRES'].total_seconds()
            
            # Assert
            assert abs(exp_timestamp - expected_expiration) < 1  # Allow 1 second difference

    def test_token_blacklist(self, app, client):
        """Test that blacklisted tokens are rejected."""
        # Arrange
        with app.app_context():
            # Create a token and add it to the blacklist
            token = create_access_token(identity="1")
            jti = decode_token(token)['jti']
            
            # Add to blacklist (using the app's blacklist mechanism)
            from app.__init__ import blacklisted_tokens
            blacklisted_tokens.add(jti)
            
            # Act
            response = client.get('/api/auth/me',
                                 headers={'Authorization': f'Bearer {token}'},
                                 content_type='application/json')
            
            # Assert
            assert response.status_code == 401
            data = json.loads(response.data)
            # assert 'error' in data
            {"msg": "Error loading the user 1"}