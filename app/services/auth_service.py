# app/services/auth_service.py
from app.models.user import User
from app import db

class AuthService:
    def authenticate_user(self, username, password):
        """Authenticate a user with username and password."""
        # Try to find user by username
        user = User.query.filter_by(username=username).first()
        
        # If user not found or password is incorrect, return None
        if not user or not user.verify_password(password):
            return None
            
        return user
        
    def get_user_by_id(self, user_id):
        """Get user by ID."""
        return User.query.get(user_id)
        
    def change_password(self, user_id, current_password, new_password):
        """Change user's password."""
        user = User.query.get(user_id)
        if not user:
            return False
            
        # Verify current password
        if not user.verify_password(current_password):
            return False
            
        # Update with new password
        user.password = new_password
        db.session.commit()
        
        return True
