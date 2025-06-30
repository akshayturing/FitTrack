# app/services/user_service.py
from app.models.user import User
from app import db

class UserService:
    def create_user(self, user_data):
        """Create a new user."""
        username = user_data.get('username')
        email = user_data.get('email')
        password = user_data.get('password')
        
        if not username or not email or not password:
            raise ValueError('Username, email, and password are required')
        
        # Check if user with this username or email already exists
        if User.query.filter_by(username=username).first():
            raise ValueError(f'Username {username} is already taken')
        
        if User.query.filter_by(email=email).first():
            raise ValueError(f'Email {email} is already registered')
        
        user = User(username=username, email=email)
        user.password = password  # This will trigger the password setter to hash it
        
        db.session.add(user)
        db.session.commit()
        
        tokens = user.generate_tokens()
        
        return user, tokens
    
    def get_user_by_id(self, user_id):
        """Get user by ID."""
        return User.query.get(user_id)
    
    def update_user(self, user_id, user_data):
        """Update user information."""
        user = User.query.get(user_id)
        if not user:
            return None
        
        # Update fields
        if 'username' in user_data and user_data['username'] != user.username:
            existing_user = User.query.filter_by(username=user_data['username']).first()
            if existing_user and existing_user.id != user.id:
                raise ValueError(f'Username {user_data["username"]} is already taken')
            user.username = user_data['username']
            
        if 'email' in user_data and user_data['email'] != user.email:
            existing_user = User.query.filter_by(email=user_data['email']).first()
            if existing_user and existing_user.id != user.id:
                raise ValueError(f'Email {user_data["email"]} is already registered')
            user.email = user_data['email']
            
        if 'password' in user_data:
            user.password = user_data['password']
        
        db.session.commit()
        return user
    
    def delete_user(self, user_id):
        """Delete a user."""
        user = User.query.get(user_id)
        if not user:
            return False
        
        db.session.delete(user)
        db.session.commit()
        return True
