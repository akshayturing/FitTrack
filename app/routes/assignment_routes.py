from flask import Blueprint, request, jsonify
from app.services.assignment_service import AssignmentService
from flask_jwt_extended import jwt_required, get_jwt_identity

assignment_bp = Blueprint('assignments', __name__)
assignment_service = AssignmentService()

@assignment_bp.route('', methods=['POST'])
@jwt_required()
def create_assignment():
    """Assign a workout to the current user."""
    # Get the current user from JWT
    current_user_id = get_jwt_identity()
    
    data = request.get_json()
    if not data or 'workout_id' not in data:
        return jsonify({'error': 'Missing workout_id in request'}), 400
    
    workout_id = data.get('workout_id')
    
    # Create the assignment
    assignment, message, status_code = assignment_service.create_assignment(
        current_user_id, workout_id
    )
    
    if status_code == 201:
        return jsonify({
            'message': message,
            'assignment': assignment.to_dict()
        }), status_code
    else:
        return jsonify({'error': message}), status_code

@assignment_bp.route('', methods=['GET'])
@jwt_required()
def get_user_assignments():
    """Get all assignments for the current user."""
    current_user_id = get_jwt_identity()
    
    # Get param for including completed assignments
    include_completed = request.args.get('include_completed', 'false').lower() == 'true'
    
    assignments = assignment_service.get_user_assignments(
        current_user_id, include_completed
    )
    
    return jsonify([a.to_dict() for a in assignments]), 200

@assignment_bp.route('/<int:assignment_id>/complete', methods=['PUT'])
@jwt_required()
def mark_assignment_complete(assignment_id):
    """Mark an assignment as completed."""
    assignment, message, status_code = assignment_service.mark_assignment_complete(
        assignment_id
    )
    
    if status_code == 200:
        return jsonify({
            'message': message,
            'assignment': assignment.to_dict()
        }), status_code
    else:
        return jsonify({'error': message}), status_code
