# app/routes/auth_routes.py
from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token, 
    create_refresh_token, 
    jwt_required, 
    current_user, 
    get_jwt_identity,
    get_jwt
)
from app.services.auth_service import AuthService

auth_bp = Blueprint('auth', __name__)
auth_service = AuthService()

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid request data'}), 400

    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    try:
        # Authenticate the user
        user = auth_service.authenticate_user(username, password)
        
        if not user:
            return jsonify({'error': 'Invalid credentials'}), 401
            
        # Create tokens
        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))
        
        return jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Refresh access token"""
    try:
        # Get the identity of the current user
        current_user_id = get_jwt_identity()
        
        # Create a new access token
        new_access_token = create_access_token(identity=current_user_id)
        
        # Return the new access token
        return jsonify({'access_token': new_access_token}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Logout by blacklisting the current token"""
    try:
        # Get the JWT token
        jti = get_jwt()['jti']
        
        # Add this token to the blacklist
        from flask import current_app
        current_app.blacklisted_tokens.add(jti)
        
        return jsonify({'message': 'Successfully logged out'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """Get the current authenticated user's details"""
    try:
        # Get user ID from JWT token
        user_id = get_jwt_identity()
        user = auth_service.get_user_by_id(user_id)
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        return jsonify(user.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/change-password', methods=['POST'])
@jwt_required()
def change_password():
    """Change user's password"""
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid request data'}), 400
        
    current_password = data.get('current_password')
    new_password = data.get('new_password')
    confirm_password = data.get('confirm_password')
    
    if not current_password or not new_password or not confirm_password:
        return jsonify({'error': 'Current password, new password, and confirm password are required'}), 400
        
    if new_password != confirm_password:
        return jsonify({'error': 'New password and confirm password must match'}), 400
        
    try:
        # Get user ID from JWT token
        user_id = get_jwt_identity()
        
        # Change password
        result = auth_service.change_password(user_id, current_password, new_password)
        
        if not result:
            return jsonify({'error': 'Failed to change password. Current password may be incorrect.'}), 400
            
        return jsonify({'message': 'Password changed successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
