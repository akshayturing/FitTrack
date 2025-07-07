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
from app.models.user import User
workout_bp = Blueprint('workouts', __name__)
workout_service = WorkoutService()
from flask import current_app
from app.models.workout import Workout
from app.models.workout_assignment import WorkoutAssignment
from app.schemas.workout_schema import workouts_schema


# @workout_bp.route('', methods=['POST'])
# @jwt_required()  # Protected endpoint
# def create_workout():
#     data = request.get_json()
#     if not data:
#         return jsonify({'error': 'Invalid request data'}), 400
    
#     # Get the current user's ID from the JWT
#     user_id = get_jwt_identity()
    
#     # Add the user_id to the workout data
#     data['user_id'] = user_id
    
#     try:
#         workout = workout_service.create_workout(data)
#         return jsonify(workout.to_dict()), 201
#     except ValueError as e:
#         return jsonify({'error': str(e)}), 400
#     except Exception as e:
#         return jsonify({'error': 'Failed to create workout'}), 500

# @workout_bp.route('/<int:workout_id>', methods=['GET'])
# @jwt_required()
# def get_workout(workout_id):
    # Get the current user's ID from the JWT
    # user_id = get_jwt_identity()
    
    # workout = workout_service.get_workout_by_id(workout_id)
    # if not workout:
    #     return jsonify({'error': 'Workout not found'}), 404
    
    # # Verify that the workout belongs to the current user
    # if workout.user_id != user_id:
    #     return jsonify({'error': 'Unauthorized access to this workout'}), 403
    
    # return jsonify(workout.to_dict()), 200

@workout_bp.route('/me', methods=['GET'])
@jwt_required()
def get_my_workouts():
    # Get the current user's ID from the JWT
    user_id = get_jwt_identity()
    
    workouts = workout_service.get_workouts_by_user(user_id)
    return jsonify([w.to_dict() for w in workouts]), 200

# @workout_bp.route('/<int:workout_id>', methods=['PUT'])
# @jwt_required()
# def update_workout(workout_id):
    # Get the current user's ID from the JWT
    # user_id = get_jwt_identity()
    
    # data = request.get_json()
    # if not data:
    #     return jsonify({'error': 'Invalid request data'}), 400
    
    # # Check if workout exists and belongs to current user
    # workout = workout_service.get_workout_by_id(workout_id)
    # if not workout:
    #     return jsonify({'error': 'Workout not found'}), 404
        
    # if workout.user_id != user_id:
    #     return jsonify({'error': 'Unauthorized access to this workout'}), 403
    
    # updated_workout = workout_service.update_workout(workout_id, data)
    # return jsonify(updated_workout.to_dict()), 200

# @workout_bp.route('/<int:workout_id>', methods=['DELETE'])
# @jwt_required()
# def delete_workout(workout_id):
#     # Get the current user's ID from the JWT
#     user_id = get_jwt_identity()
    
#     # Check if workout exists and belongs to current user
#     workout = workout_service.get_workout_by_id(workout_id)
#     if not workout:
#         return jsonify({'error': 'Workout not found'}), 404
        
#     if workout.user_id != user_id:
#         return jsonify({'error': 'Unauthorized access to this workout'}), 403
        
#     if workout_service.delete_workout(workout_id):
#         return jsonify({'message': 'Workout deleted successfully'}), 200
    
#     return jsonify({'error': 'Failed to delete workout'}), 500

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

@workout_bp.route('/users/<int:user_id>/workouts', methods=['GET'])
@jwt_required()
def get_user_workouts_api(user_id):
    """
    API endpoint to get all workouts assigned to a user.
    JWT authenticated version.
    """
    # Get user ID from JWT token
    current_user_id = get_jwt_identity()
    print(current_user_id)
    # Get the authenticated user to check for admin status
    current_user = User.query.get(current_user_id)
    if not current_user:
        return jsonify({"error": "User not found"}), 404
    
    # Check if the user is requesting their own workouts or is an admin
    if current_user_id != user_id and not getattr(current_user, 'is_admin', False):
        return jsonify({"error": "Unauthorized access"}), 403
    
    try:
        # Check if requested user exists
        requested_user = User.query.get(user_id)
        if not requested_user:
            return jsonify({"error": "Requested user not found"}), 404
            
        # Get all workout assignments for the user
        assignments = WorkoutAssignment.query.filter_by(user_id=user_id, is_active=True).all()
        
        # Extract workout IDs from assignments
        workout_ids = [assignment.workout_id for assignment in assignments]
        
        # Get all relevant workouts
        workouts = Workout.query.filter(Workout.id.in_(workout_ids)).all() if workout_ids else []
        
        # Return serialized workouts
        return jsonify({"workouts": workouts_schema.dump(workouts)}), 200
    except Exception as e:
        current_app.logger.error(f"Error fetching user workouts: {str(e)}")
        return jsonify({"error": f"Failed to fetch workouts: {str(e)}"}), 500
    
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