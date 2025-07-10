# app/auth/jwt_callbacks.py
from flask import jsonify
from app.models.revoked_token import RevokedToken
from app.models.user import User
from app import db
def register_jwt_callbacks(jwt):
    """Register callbacks for Flask-JWT-Extended"""
    
    # This function will be called whenever a protected endpoint is accessed
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return db.session.get(User, identity)#User.query.get(identity)
    
    # Check if a token is revoked
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(_jwt_header, jwt_data):
        jti = jwt_data["jti"]
        return RevokedToken.is_token_revoked(jti)
    
    # Return custom response when token is revoked
    @jwt.revoked_token_loader
    def revoked_token_callback(_jwt_header, _jwt_data):
        return jsonify({
            'error': 'Token has been revoked',
            'code': 'token_revoked'
        }), 401
    
    # Return custom response when token is expired
    @jwt.expired_token_loader
    def expired_token_callback(_jwt_header, _jwt_data):
        return jsonify({
            'error': 'Token has expired',
            'code': 'token_expired'
        }), 401
    
    # Return custom response when no token is provided
    @jwt.unauthorized_loader
    def missing_token_callback(error_string):
        return jsonify({
            'error': error_string,
            'code': 'authorization_required'
        }), 401
    
    # Return custom response when invalid token is provided
    @jwt.invalid_token_loader
    def invalid_token_callback(error_string):
        return jsonify({
            'error': error_string,
            'code': 'invalid_token'
        }), 401