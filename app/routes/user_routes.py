# app/routes/user_routes.py
from flask import Blueprint, request, jsonify
from app.services.user_service import UserService
from app import db

user_bp = Blueprint('users', __name__)
user_service = UserService()

@user_bp.route('', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid request data'}), 400
    
    try:
        user = user_service.create_user(data)
        return jsonify(user.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Failed to create user'}), 500

@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = user_service.get_user_by_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user.to_dict()), 200

@user_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid request data'}), 400
    
    user = user_service.update_user(user_id, data)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user.to_dict()), 200

@user_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_service.delete_user(user_id):
        return jsonify({'message': 'User deleted successfully'}), 200
    return jsonify({'error': 'User not found'}), 404
