# # app/routes/workout_routes.py
# from flask import Blueprint, request, jsonify
# from app.services.workout_service import WorkoutService

# workout_bp = Blueprint('workouts', __name__)
# workout_service = WorkoutService()

# @workout_bp.route('', methods=['POST'])
# def create_workout():
#     data = request.get_json()
#     if not data:
#         return jsonify({'error': 'Invalid request data'}), 400
    
#     try:
#         workout = workout_service.create_workout(data)
#         return jsonify(workout.to_dict()), 201
#     except ValueError as e:
#         return jsonify({'error': str(e)}), 400
#     except Exception as e:
#         return jsonify({'error': 'Failed to create workout'}), 500

# @workout_bp.route('/<int:workout_id>', methods=['GET'])
# def get_workout(workout_id):
#     workout = workout_service.get_workout_by_id(workout_id)
#     if not workout:
#         return jsonify({'error': 'Workout not found'}), 404
    
#     return jsonify(workout.to_dict()), 200

# @workout_bp.route('/user/<int:user_id>', methods=['GET'])
# def get_user_workouts(user_id):
#     workouts = workout_service.get_workouts_by_user(user_id)
#     return jsonify([w.to_dict() for w in workouts]), 200

# @workout_bp.route('/<int:workout_id>', methods=['PUT'])
# def update_workout(workout_id):
#     data = request.get_json()
#     if not data:
#         return jsonify({'error': 'Invalid request data'}), 400
    
#     workout = workout_service.update_workout(workout_id, data)
#     if not workout:
#         return jsonify({'error': 'Workout not found'}), 404
    
#     return jsonify(workout.to_dict()), 200

# @workout_bp.route('/<int:workout_id>', methods=['DELETE'])
# def delete_workout(workout_id):
#     if workout_service.delete_workout(workout_id):
#         return jsonify({'message': 'Workout deleted successfully'}), 200
#     return jsonify({'error': 'Workout not found'}), 404

# app/routes/workout_routes.py
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.workout_service import WorkoutService
from flask_jwt_extended import jwt_required, current_user

workout_bp = Blueprint('workouts', __name__)
workout_service = WorkoutService()

@workout_bp.route('', methods=['POST'])
@jwt_required()  # Protected endpoint
def create_workout():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid request data'}), 400
    
    # Get the current user's ID from the JWT
    user_id = get_jwt_identity()
    
    # Add the user_id to the workout data
    data['user_id'] = user_id
    
    try:
        workout = workout_service.create_workout(data)
        return jsonify(workout.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Failed to create workout'}), 500

@workout_bp.route('/<int:workout_id>', methods=['GET'])
@jwt_required()
def get_workout(workout_id):
    # Get the current user's ID from the JWT
    user_id = get_jwt_identity()
    
    workout = workout_service.get_workout_by_id(workout_id)
    if not workout:
        return jsonify({'error': 'Workout not found'}), 404
    
    # Verify that the workout belongs to the current user
    if workout.user_id != user_id:
        return jsonify({'error': 'Unauthorized access to this workout'}), 403
    
    return jsonify(workout.to_dict()), 200

@workout_bp.route('/me', methods=['GET'])
@jwt_required()
def get_my_workouts():
    # Get the current user's ID from the JWT
    user_id = get_jwt_identity()
    
    workouts = workout_service.get_workouts_by_user(user_id)
    return jsonify([w.to_dict() for w in workouts]), 200

@workout_bp.route('/<int:workout_id>', methods=['PUT'])
@jwt_required()
def update_workout(workout_id):
    # Get the current user's ID from the JWT
    user_id = get_jwt_identity()
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid request data'}), 400
    
    # Check if workout exists and belongs to current user
    workout = workout_service.get_workout_by_id(workout_id)
    if not workout:
        return jsonify({'error': 'Workout not found'}), 404
        
    if workout.user_id != user_id:
        return jsonify({'error': 'Unauthorized access to this workout'}), 403
    
    updated_workout = workout_service.update_workout(workout_id, data)
    return jsonify(updated_workout.to_dict()), 200

@workout_bp.route('/<int:workout_id>', methods=['DELETE'])
@jwt_required()
def delete_workout(workout_id):
    # Get the current user's ID from the JWT
    user_id = get_jwt_identity()
    
    # Check if workout exists and belongs to current user
    workout = workout_service.get_workout_by_id(workout_id)
    if not workout:
        return jsonify({'error': 'Workout not found'}), 404
        
    if workout.user_id != user_id:
        return jsonify({'error': 'Unauthorized access to this workout'}), 403
        
    if workout_service.delete_workout(workout_id):
        return jsonify({'message': 'Workout deleted successfully'}), 200
    
    return jsonify({'error': 'Failed to delete workout'}), 500

@workout_bp.route('', methods=['POST'])
@jwt_required()
def create_workout():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid request data'}), 400
    
    # Ensure the workout is created for the current user
    data['user_id'] = current_user.id
    
    try:
        workout = workout_service.create_workout(data)
        return jsonify(workout.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Failed to create workout'}), 500

@workout_bp.route('/<int:workout_id>', methods=['GET'])
@jwt_required()
def get_workout(workout_id):
    workout = workout_service.get_workout_by_id(workout_id)
    if not workout:
        return jsonify({'error': 'Workout not found'}), 404
    
    # Only allow users to view their own workouts
    if workout.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized access'}), 403
    
    return jsonify(workout.to_dict()), 200

@workout_bp.route('/user/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_workouts(user_id):
    # Only allow users to view their own workouts
    if user_id != current_user.id:
        return jsonify({'error': 'Unauthorized access'}), 403
        
    workouts = workout_service.get_workouts_by_user(user_id)
    return jsonify([w.to_dict() for w in workouts]), 200

@workout_bp.route('/<int:workout_id>', methods=['PUT'])
@jwt_required()
def update_workout(workout_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid request data'}), 400
    
    workout = workout_service.get_workout_by_id(workout_id)
    if not workout:
        return jsonify({'error': 'Workout not found'}), 404
    
    # Only allow users to update their own workouts
    if workout.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized access'}), 403
    
    updated_workout = workout_service.update_workout(workout_id, data)
    return jsonify(updated_workout.to_dict()), 200

@workout_bp.route('/<int:workout_id>', methods=['DELETE'])
@jwt_required()
def delete_workout(workout_id):
    workout = workout_service.get_workout_by_id(workout_id)
    if not workout:
        return jsonify({'error': 'Workout not found'}), 404
    
    # Only allow users to delete their own workouts
    if workout.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized access'}), 403
    
    if workout_service.delete_workout(workout_id):
        return jsonify({'message': 'Workout deleted successfully'}), 200
    return jsonify({'error': 'Failed to delete workout'}), 500