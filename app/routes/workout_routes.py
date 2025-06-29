# app/routes/workout_routes.py
from flask import Blueprint, request, jsonify
from app.services.workout_service import WorkoutService

workout_bp = Blueprint('workouts', __name__)
workout_service = WorkoutService()

@workout_bp.route('', methods=['POST'])
def create_workout():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid request data'}), 400
    
    try:
        workout = workout_service.create_workout(data)
        return jsonify(workout.to_dict()), 201
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': 'Failed to create workout'}), 500

@workout_bp.route('/<int:workout_id>', methods=['GET'])
def get_workout(workout_id):
    workout = workout_service.get_workout_by_id(workout_id)
    if not workout:
        return jsonify({'error': 'Workout not found'}), 404
    
    return jsonify(workout.to_dict()), 200

@workout_bp.route('/user/<int:user_id>', methods=['GET'])
def get_user_workouts(user_id):
    workouts = workout_service.get_workouts_by_user(user_id)
    return jsonify([w.to_dict() for w in workouts]), 200

@workout_bp.route('/<int:workout_id>', methods=['PUT'])
def update_workout(workout_id):
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid request data'}), 400
    
    workout = workout_service.update_workout(workout_id, data)
    if not workout:
        return jsonify({'error': 'Workout not found'}), 404
    
    return jsonify(workout.to_dict()), 200

@workout_bp.route('/<int:workout_id>', methods=['DELETE'])
def delete_workout(workout_id):
    if workout_service.delete_workout(workout_id):
        return jsonify({'message': 'Workout deleted successfully'}), 200
    return jsonify({'error': 'Workout not found'}), 404
