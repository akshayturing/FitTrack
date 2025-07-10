# app/auth/auth_service.py
from app.models.user import User
from app.models.revoked_token import RevokedToken
from flask_jwt_extended import get_jwt, get_jti, decode_token, create_access_token
from datetime import datetime, timezone
from app import db
class AuthService:
    @staticmethod
    def authenticate(username, password):
        """Authenticate a user by username/email and password"""
        # Try to find the user by username
        user = User.get_user_by_username(username)
        
        # If not found, try email
        if not user:
            user = User.get_user_by_email(username)
        
        # Check if user exists and password matches
        if user and user.verify_password(password):
            return user.generate_tokens()
        
        return None

    @staticmethod
    def refresh_access_token(refresh_token):
        """Create a new access token from a refresh token"""
        try:
            # Decode the refresh token to get the user ID
            decoded_token = decode_token(refresh_token)
            user_id = decoded_token['sub']
            
            # Check if the token is in the blocklist
            jti = decoded_token['jti']
            if RevokedToken.is_token_revoked(jti):
                return None
            
            # Get the user
            user = db.session.get(User, user_id)
            if not user:
                return None
                
            # Create a new access token
            access_token = create_access_token(identity=str(user.id))
            return {
                'access_token': access_token,
                'user': user.to_dict()
            }
        except Exception:
            return None
    
    @staticmethod
    def logout(token_jti, expires_at):
        """Add a token to the revoked tokens list"""
        RevokedToken.revoke_token(token_jti, expires_at)
        
        # Maintenance: clean up expired tokens
        try:
            RevokedToken.prune_expired_tokens()
        except Exception as e:
            # Just log the error, don't affect the logout operation
            print(f"Error pruning expired tokens: {e}")
