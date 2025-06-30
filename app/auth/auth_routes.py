# app/auth/auth_routes.py
from flask import Blueprint, request, jsonify
from app.auth.auth_service import AuthService
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity, current_user
from datetime import datetime, timezone

auth_bp = Blueprint('auth', __name__)
auth_service = AuthService()

@auth_bp.route('/login', methods=['POST'])
def login():
    """Login and get tokens"""
    if not request.is_json:
        return jsonify({"error": "Missing JSON in request"}), 400
    
    username = request.json.get('username')
    password = request.json.get('password')
    
    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400
    
    tokens = auth_service.authenticate(username, password)
    
    if not tokens:
        return jsonify({"error": "Invalid username or password"}), 401
    
    return jsonify(tokens), 200

@auth_bp.route('/refresh', methods=['POST'])
def refresh():
    """Refresh access token"""
    if not request.is_json:
        return jsonify({"error": "Missing JSON in request"}), 400
    
    refresh_token = request.json.get('refresh_token')
    
    if not refresh_token:
        return jsonify({"error": "Missing refresh token"}), 400
    
    tokens = auth_service.refresh_access_token(refresh_token)
    
    if not tokens:
        return jsonify({"error": "Invalid or expired refresh token"}), 401
    
    return jsonify(tokens), 200

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Logout and revoke tokens"""
    jwt_data = get_jwt()
    jti = jwt_data["jti"]
    exp = datetime.fromtimestamp(jwt_data["exp"], timezone.utc)
    
    auth_service.logout(jti, exp)
    
    return jsonify({"message": "Successfully logged out"}), 200

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_user_info():
    """Get current user info"""
    return jsonify(current_user.to_dict()), 200
