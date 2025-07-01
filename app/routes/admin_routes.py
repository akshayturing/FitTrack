from flask import Blueprint, request, jsonify, current_app
from app.models.exercise import Exercise, ExerciseType
from app import db
from functools import wraps

admin_bp = Blueprint('admin', __name__)

# Admin authorization middleware
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get the API key from the header
        api_key = request.headers.get('X-API-Key')
        
        if not api_key:
            return jsonify({
                'status': 'error',
                'message': 'API key is missing'
            }), 401
        
        # Check if the API key is valid (in production, use a more secure method)
        valid_api_key = current_app.config.get('ADMIN_API_KEY', 'admin-secret-key')
        
        if api_key != valid_api_key:
            return jsonify({
                'status': 'error',
                'message': 'Invalid API key'
            }), 403
                
        # API key is valid, proceed with the request
        return f(*args, **kwargs)
            
    return decorated_function

# CREATE - Add a new exercise
@admin_bp.route('/exercises', methods=['POST'])
@admin_required
def create_exercise():
    data = request.get_json()
    
    if not data:
        return jsonify({
            'status': 'error',
            'message': 'No input data provided'
        }), 400
    
    # Validate required fields
    required_fields = ['name', 'type']
    for field in required_fields:
        if field not in data:
            return jsonify({
                'status': 'error',
                'message': f'Missing required field: {field}'
            }), 400
    
    # Validate exercise type
    try:
        exercise_type = ExerciseType(data['type'])
    except ValueError:
        valid_types = [t.value for t in ExerciseType]
        return jsonify({
            'status': 'error',
            'message': f'Invalid exercise type. Valid types are: {", ".join(valid_types)}'
        }), 400
    
    # Check for duplicate names
    existing_exercise = Exercise.query.filter_by(name=data['name']).first()
    if existing_exercise:
        return jsonify({
            'status': 'error',
            'message': f'Exercise with name "{data["name"]}" already exists'
        }), 409  # Conflict status code
    
    # Create the exercise
    exercise = Exercise(
        name=data['name'],
        type=exercise_type,
        description=data.get('description'),
        default_reps=data.get('default_reps'),
        default_sets=data.get('default_sets'),
        target_muscles=data.get('target_muscles'),
        instructions=data.get('instructions')
    )
    
    try:
        db.session.add(exercise)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Exercise created successfully',
            'data': {
                'id': exercise.id,
                'name': exercise.name,
                'type': exercise.type.value,
                'description': exercise.description,
                'default_reps': exercise.default_reps,
                'default_sets': exercise.default_sets,
                'target_muscles': exercise.target_muscles,
                'instructions': exercise.instructions
            }
        }), 201  # Created status code
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error creating exercise: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': 'An error occurred while creating the exercise'
        }), 500

# READ (list) - Get all exercises
@admin_bp.route('/exercises', methods=['GET'])
@admin_required
def get_exercises():
    # Allow filtering by type
    exercise_type = request.args.get('type')
    
    query = Exercise.query
    if exercise_type:
        try:
            type_enum = ExerciseType(exercise_type)
            query = query.filter_by(type=type_enum)
        except ValueError:
            pass  # Ignore invalid type filters
    
    exercises = query.all()
    
    # Format response
    exercises_list = []
    for ex in exercises:
        exercises_list.append({
            'id': ex.id,
            'name': ex.name,
            'type': ex.type.value,
            'description': ex.description,
            'default_reps': ex.default_reps,
            'default_sets': ex.default_sets,
            'target_muscles': ex.target_muscles,
            'instructions': ex.instructions
        })
    
    return jsonify({
        'status': 'success',
        'count': len(exercises_list),
        'data': exercises_list
    }), 200

# READ (single) - Get a specific exercise
@admin_bp.route('/exercises/<int:exercise_id>', methods=['GET'])
@admin_required
def get_exercise(exercise_id):
    exercise = Exercise.query.get(exercise_id)
    
    if not exercise:
        return jsonify({
            'status': 'error',
            'message': f'Exercise with id {exercise_id} not found'
        }), 404
    
    # Format response
    exercise_data = {
        'id': exercise.id,
        'name': exercise.name,
        'type': exercise.type.value,
        'description': exercise.description,
        'default_reps': exercise.default_reps,
        'default_sets': exercise.default_sets,
        'target_muscles': exercise.target_muscles,
        'instructions': exercise.instructions
    }
    
    return jsonify({
        'status': 'success',
        'data': exercise_data
    }), 200

# UPDATE - Modify an existing exercise
@admin_bp.route('/exercises/<int:exercise_id>', methods=['PUT'])
@admin_required
def update_exercise(exercise_id):
    exercise = Exercise.query.get(exercise_id)
    
    if not exercise:
        return jsonify({
            'status': 'error',
            'message': f'Exercise with id {exercise_id} not found'
        }), 404
    
    data = request.get_json()
    
    if not data:
        return jsonify({
            'status': 'error',
            'message': 'No input data provided'
        }), 400
    
    # Update exercise type if provided
    if 'type' in data:
        try:
            exercise.type = ExerciseType(data['type'])
        except ValueError:
            valid_types = [t.value for t in ExerciseType]
            return jsonify({
                'status': 'error',
                'message': f'Invalid exercise type. Valid types are: {", ".join(valid_types)}'
            }), 400
    
    # Update name if provided (with duplicate check)
    if 'name' in data and data['name'] != exercise.name:
        existing_exercise = Exercise.query.filter_by(name=data['name']).first()
        if existing_exercise and existing_exercise.id != exercise_id:
            return jsonify({
                'status': 'error',
                'message': f'Exercise with name "{data["name"]}" already exists'
            }), 409
        exercise.name = data['name']
    
    # Update other fields if provided
    for field in ['description', 'default_reps', 'default_sets', 'target_muscles', 'instructions']:
        if field in data:
            setattr(exercise, field, data[field])
    
    try:
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': 'Exercise updated successfully',
            'data': {
                'id': exercise.id,
                'name': exercise.name,
                'type': exercise.type.value,
                'description': exercise.description,
                'default_reps': exercise.default_reps,
                'default_sets': exercise.default_sets,
                'target_muscles': exercise.target_muscles,
                'instructions': exercise.instructions
            }
        }), 200
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error updating exercise: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': 'An error occurred while updating the exercise'
        }), 500

# DELETE - Remove an exercise
@admin_bp.route('/exercises/<int:exercise_id>', methods=['DELETE'])
@admin_required
def delete_exercise(exercise_id):
    exercise = Exercise.query.get(exercise_id)
    
    if not exercise:
        return jsonify({
            'status': 'error',
            'message': f'Exercise with id {exercise_id} not found'
        }), 404
    
    try:
        db.session.delete(exercise)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': f'Exercise with id {exercise_id} has been deleted'
        }), 200
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error deleting exercise: {str(e)}')
        
        return jsonify({
            'status': 'error',
            'message': 'An error occurred while deleting the exercise'
        }), 500