# app/routes/user_routes.py
from flask import Blueprint, request, jsonify
from app.services.user_service import UserService
from app import db
from flask_jwt_extended import jwt_required, current_user
user_bp = Blueprint('users', __name__)
user_service = UserService()

@user_bp.route('', methods=['POST'])
def create_user():
    data = request.get_json()
    print(data)
    if not data:
        return jsonify({'error': 'Invalid request data'}), 400
    
    try:
        user = user_service.create_user(data)
        return jsonify(user.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Failed to create user'}), 500

# @user_bp.route('/<int:user_id>', methods=['GET'])
# def get_user(user_id):
#     user = user_service.get_user_by_id(user_id)
#     if not user:
#         return jsonify({'error': 'User not found'}), 404
    
#     return jsonify(user.to_dict()), 200

# @user_bp.route('/<int:user_id>', methods=['PUT'])
# def update_user(user_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid request data'}), 400
    
    user = user_service.update_user(user_id, data)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user.to_dict()), 200

# @user_bp.route('/<int:user_id>', methods=['DELETE'])
# def delete_user(user_id):
    if user_service.delete_user(user_id):
        return jsonify({'message': 'User deleted successfully'}), 200
    return jsonify({'error': 'User not found'}), 404

# @user_bp.route('/register', methods=['POST'])
# def register_user():
#     data = request.get_json()
#     if not data:
#         return jsonify({'error': 'Invalid request data'}), 400
    
#     try:
#         user, tokens = user_service.validate_and_register_user(data)
#         # Return tokens along with user data
#         return jsonify(tokens), 201
#     except ValueError as e:
#         return jsonify({'error': str(e)}), 400
#     except Exception as e:
#         return jsonify({'error': 'Failed to register user'}), 500
    
@user_bp.route('/register', methods=['POST'])
def register_user():
    print("coing here")
    data = request.get_json()
    print(data)
    if not data:
        return jsonify({'error': 'Invalid request data'}), 400
    
    try:
        user, tokens = user_service.create_user(data)
        # Return tokens along with user data
        return jsonify(tokens), 201
    except ValueError as e:
        # This catches validation errors
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        # Add detailed error logging
        import traceback
        print(f"Registration error: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': f'Failed to register user: {str(e)}'}), 500
@user_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    # Only allow users to access their own data or admins to access any data
    if current_user.id != user_id:
        return jsonify({'error': 'Unauthorized access'}), 403
        
    user = user_service.get_user_by_id(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user.to_dict()), 200

@user_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    # Only allow users to update their own data
    if current_user.id != user_id:
        return jsonify({'error': 'Unauthorized access'}), 403
        
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid request data'}), 400
    
    user = user_service.update_user(user_id, data)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user.to_dict()), 200

@user_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    # Only allow users to delete their own account
    if current_user.id != user_id:
        return jsonify({'error': 'Unauthorized access'}), 403
        
    if user_service.delete_user(user_id):
        return jsonify({'message': 'User deleted successfully'}), 200
    return jsonify({'error': 'User not found'}), 404