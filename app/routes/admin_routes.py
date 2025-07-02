from flask import Blueprint, request, jsonify, current_app
from app.models.exercise import Exercise, ExerciseType
from app import db
from functools import wraps
from app.models.workout import Workout
from app.models.workout_exercise import  WorkoutExercise
from app.models.exercise import Exercise
from app.services.workout_service import WorkoutService

admin_bp = Blueprint('admin', __name__)
workout_service = WorkoutService()
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
    exercise = db.session.get(Exercise, exercise_id) #Exercise.query.get(exercise_id)
    
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
    exercise = db.session.get(Exercise, exercise_id) #Exercise.query.get(exercise_id)
    
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
    exercise = db.session.get(Exercise, exercise_id) #Exercise.query.get(exercise_id)
    
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
    
@admin_bp.route('/workouts', methods=['POST'])
@admin_required
def create_workout():
    data = request.get_json()
    print("########################")
    print(data)
    print("########################")
    if not data:
        return jsonify({
            'status': 'error',
            'message': 'No input data provided'
        }), 400
    
    # Validate required fields
    required_fields = ['name', 'user_id']
    for field in required_fields:
        if field not in data:
            return jsonify({
                'status': 'error',
                'message': f'Missing required field: {field}'
            }), 400
    
    # Check if user exists
    from app.models.user import User
    user = db.session.get(User, data['user_id']) #User.query.get(data['user_id'])
    if not user:
        return jsonify({
            'status': 'error',
            'message': f'User with id {data["user_id"]} not found'
        }), 404
    
    # Create the workout
    workout = Workout(
        title=data['name'],
        description=data.get('description'),
        user_id=data['user_id'],
        workout_type=data.get('workout_type')
    )
    
    # Process attached exercises if provided
    exercises_data = data.get('exercises', [])
    if not isinstance(exercises_data, list):
        return jsonify({
            'status': 'error',
            'message': 'Exercises must be provided as a list'
        }), 400
    
    # Track errors for invalid exercises
    invalid_exercises = []
    
    # Add exercises to the workout
    for i, ex_data in enumerate(exercises_data):
        # Validate exercise data structure
        if not isinstance(ex_data, dict):
            invalid_exercises.append({
                'index': i,
                'error': 'Exercise data must be an object'
            })
            continue
            
        # Validate required exercise fields
        if 'exercise_id' not in ex_data:
            invalid_exercises.append({
                'index': i,
                'error': 'Missing exercise_id'
            })
            continue
            
        # Check if exercise exists
        exercise = db.session.get(Exercise, ex_data['exercise_id']) #Exercise.query.get(ex_data['exercise_id'])
        if not exercise:
            invalid_exercises.append({
                'index': i,
                'error': f'Exercise with id {ex_data["exercise_id"]} not found'
            })
            continue
        
        # Create workout exercise relationship
        workout_exercise = WorkoutExercise(
            exercise_id=ex_data['exercise_id'],
            position=i+1,  # Use index+1 as position if not specified
            custom_sets=ex_data.get('custom_sets'),
            custom_reps=ex_data.get('custom_reps'),
            notes=ex_data.get('notes')
        )
        
        workout.workout_exercises.append(workout_exercise)
    
    # If there were invalid exercises, return error with details
    if invalid_exercises:
        return jsonify({
            'status': 'error',
            'message': 'Invalid exercises in request',
            'errors': invalid_exercises
        }), 400
    
    try:
        db.session.add(workout)
        db.session.commit()
        
        # Format response
        workout_data = format_workout_response(workout)
        
        return jsonify({
            'status': 'success',
            'message': 'Workout created successfully',
            'data': workout_data
        }), 201
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error creating workout: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': f'An error occurred while creating the workout: {str(e)}'
        }), 500

# Helper function to format workout responses consistently
def format_workout_response(workout):
    exercises = []
    for we in workout.workout_exercises:
        exercise = we.exercise
        exercises.append({
            'id': we.id,
            'exercise_id': exercise.id,
            'exercise_name': exercise.name,
            'exercise_type': exercise.type.value,
            'position': we.position,
            'sets': we.custom_sets or exercise.default_sets,
            'reps': we.custom_reps or exercise.default_reps,
            'notes': we.notes
        })
        
    return {
        'id': workout.id,
        'name': workout.name,
        'description': workout.description,
        'user_id': workout.user_id,
        'workout_type': workout.workout_type,
        'created_at': workout.created_at.isoformat() if workout.created_at else None,
        'exercises': exercises
    }

# READ (list) - Get all workouts
@admin_bp.route('/workouts', methods=['GET'])
@admin_required
def get_workouts():
    # Support filtering by user
    user_id = request.args.get('user_id')
    
    query = Workout.query
    if user_id:
        try:
            query = query.filter_by(user_id=int(user_id))
        except ValueError:
            return jsonify({
                'status': 'error',
                'message': 'Invalid user_id parameter'
            }), 400
    
    workouts = query.all()
    
    # Format response
    workouts_list = [format_workout_response(workout) for workout in workouts]
    
    return jsonify({
        'status': 'success',
        'count': len(workouts_list),
        'data': workouts_list
    }), 200

# READ (single) - Get a specific workout
@admin_bp.route('/workouts/<int:workout_id>', methods=['GET'])
@admin_required
def get_workout(workout_id):
    workout = db.session.get(Workout, workout_id) #Workout.query.get(workout_id)
    
    if not workout:
        return jsonify({
            'status': 'error',
            'message': f'Workout with id {workout_id} not found'
        }), 404
    
    # Format response
    workout_data = format_workout_response(workout)
    
    return jsonify({
        'status': 'success',
        'data': workout_data
    }), 200

# UPDATE - Modify an existing workout and its exercises
@admin_bp.route('/workouts/<int:workout_id>', methods=['PUT'])
@admin_required
def update_workout(workout_id):
    workout = db.session.get(Workout, workout_id)#Workout.query.get(workout_id)
    
    if not workout:
        return jsonify({
            'status': 'error',
            'message': f'Workout with id {workout_id} not found'
        }), 404
    
    data = request.get_json()
    
    if not data:
        return jsonify({
            'status': 'error',
            'message': 'No input data provided'
        }), 400
    
    # Update user if provided
    if 'user_id' in data:
        from app.models.user import User
        user = db.session.get(User, data['user_id']) #User.query.get(data['user_id'])
        if not user:
            return jsonify({
                'status': 'error',
                'message': f'User with id {data["user_id"]} not found'
            }), 404
        workout.user_id = data['user_id']
    
    # Update other fields if provided
    for field in ['name', 'description', 'workout_type', 'duration']:
        if field in data:
            setattr(workout, field, data[field])
    
    # Update exercises if provided
    if 'exercises' in data:
        exercises_data = data['exercises']
        
        if not isinstance(exercises_data, list):
            return jsonify({
                'status': 'error',
                'message': 'Exercises must be provided as a list'
            }), 400
        
        # Track errors for invalid exercises
        invalid_exercises = []
        
        # Clear existing exercises if we're replacing them completely
        for we in workout.workout_exercises:
            db.session.delete(we)
        
        # Add new exercises to the workout
        for i, ex_data in enumerate(exercises_data):
            # Validate exercise data structure
            if not isinstance(ex_data, dict):
                invalid_exercises.append({
                    'index': i,
                    'error': 'Exercise data must be an object'
                })
                continue
                
            # Validate required exercise fields
            if 'exercise_id' not in ex_data:
                invalid_exercises.append({
                    'index': i,
                    'error': 'Missing exercise_id'
                })
                continue
                
            # Check if exercise exists
            exercise = db.session.get(Exercise, ex_data['exercise_id']) #Exercise.query.get(ex_data['exercise_id'])
            if not exercise:
                invalid_exercises.append({
                    'index': i,
                    'error': f'Exercise with id {ex_data["exercise_id"]} not found'
                })
                continue
            
            # Create workout exercise relationship
            workout_exercise = WorkoutExercise(
                workout_id=workout.id,
                exercise_id=ex_data['exercise_id'],
                position=i+1,  # Use index+1 as position by default
                custom_sets=ex_data.get('custom_sets'),
                custom_reps=ex_data.get('custom_reps'),
                notes=ex_data.get('notes')
            )
            
            workout.workout_exercises.append(workout_exercise)
        
        # If there were invalid exercises, return error with details
        if invalid_exercises:
            db.session.rollback()
            return jsonify({
                'status': 'error',
                'message': 'Invalid exercises in request',
                'errors': invalid_exercises
            }), 400
    
    try:
        db.session.commit()
        
        # Format response
        workout_data = format_workout_response(workout)
        
        return jsonify({
            'status': 'success',
            'message': 'Workout updated successfully',
            'data': workout_data
        }), 200
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error updating workout: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': f'An error occurred while updating the workout: {str(e)}'
        }), 500

# DELETE - Remove a workout
@admin_bp.route('/workouts/<int:workout_id>', methods=['DELETE'])
@admin_required
def delete_workout(workout_id):
    workout = db.session.get(Workout, workout_id) # Workout.query.get(workout_id)
    
    if not workout:
        return jsonify({
            'status': 'error',
            'message': f'Workout with id {workout_id} not found'
        }), 404
    
    try:
        db.session.delete(workout)
        db.session.commit()
        
        return jsonify({
            'status': 'success',
            'message': f'Workout with id {workout_id} has been deleted'
        }), 200
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error deleting workout: {str(e)}')
        
        return jsonify({
            'status': 'error',
            'message': f'An error occurred while deleting the workout: {str(e)}'
        }), 500

# ADDITIONAL ENDPOINT - Manage exercises in a workout
@admin_bp.route('/workouts/<int:workout_id>/exercises', methods=['POST'])
@admin_required
def add_exercise_to_workout(workout_id):
    """Add a single exercise to an existing workout"""
    workout = db.session.get(Workout, workout_id)#(workout_id)
    
    if not workout:
        return jsonify({
            'status': 'error',
            'message': f'Workout with id {workout_id} not found'
        }), 404
    
    data = request.get_json()
    
    if not data:
        return jsonify({
            'status': 'error',
            'message': 'No input data provided'
        }), 400
    
    # Validate required fields
    if 'exercise_id' not in data:
        return jsonify({
            'status': 'error',
            'message': 'Missing required field: exercise_id'
        }), 400
    
    # Check if exercise exists
    exercise = db.session.get(Exercise, data['exercise_id']) #Exercise.query.get(data['exercise_id'])
    if not exercise:
        return jsonify({
            'status': 'error',
            'message': f'Exercise with id {data["exercise_id"]} not found'
        }), 404
    
    # Determine position (either specified or at the end)
    position = data.get('position')
    if position is None:
        # Get the highest position and add 1
        highest_position = db.session.query(db.func.max(WorkoutExercise.position))\
            .filter_by(workout_id=workout_id).scalar() or 0
        position = highest_position + 1
    
    # If a position is specified, we need to shift existing exercises
    else:
        # Ensure position is an integer
        try:
            position = int(position)
            if position < 1:
                return jsonify({
                    'status': 'error',
                    'message': 'Position must be a positive integer'
                }), 400
        except ValueError:
            return jsonify({
                'status': 'error',
                'message': 'Position must be a positive integer'
            }), 400
        
        # Shift positions of existing exercises
        db.session.query(WorkoutExercise)\
            .filter(WorkoutExercise.workout_id == workout_id, 
                   WorkoutExercise.position >= position)\
            .update({WorkoutExercise.position: WorkoutExercise.position + 1}, 
                   synchronize_session=False)
    
    # Create workout exercise relationship
    workout_exercise = WorkoutExercise(
        workout_id=workout.id,
        exercise_id=data['exercise_id'],
        position=position,
        custom_sets=data.get('custom_sets'),
        custom_reps=data.get('custom_reps'),
        notes=data.get('notes')
    )
    
    try:
        db.session.add(workout_exercise)
        db.session.commit()
        
        # Refresh the workout to get updated exercise list
        db.session.refresh(workout)
        
        # Format response
        workout_data = format_workout_response(workout)
        
        return jsonify({
            'status': 'success',
            'message': 'Exercise added to workout',
            'data': workout_data
        }), 201
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error adding exercise to workout: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': f'An error occurred while adding the exercise: {str(e)}'
        }), 500

# Remove an exercise from a workout
@admin_bp.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>', methods=['DELETE'])
@admin_required
def remove_exercise_from_workout(workout_id, exercise_id):
    """Remove an exercise from a workout and reorder remaining exercises"""
    workout = db.session.get(Workout, workout_id) #Workout.query.get(workout_id)
    
    if not workout:
        return jsonify({
            'status': 'error',
            'message': f'Workout with id {workout_id} not found'
        }), 404
    
    # Find the workout exercise
    workout_exercise = WorkoutExercise.query\
        .filter_by(workout_id=workout_id, exercise_id=exercise_id)\
        .first()
    
    if not workout_exercise:
        return jsonify({
            'status': 'error',
            'message': f'Exercise with id {exercise_id} not found in this workout'
        }), 404
    
    removed_position = workout_exercise.position
    
    try:
        # Delete the workout exercise
        db.session.delete(workout_exercise)
        
        # Reorder remaining exercises
        db.session.query(WorkoutExercise)\
            .filter(WorkoutExercise.workout_id == workout_id, 
                   WorkoutExercise.position > removed_position)\
            .update({WorkoutExercise.position: WorkoutExercise.position - 1}, 
                   synchronize_session=False)
        
        db.session.commit()
        
        # Refresh the workout to get updated exercise list
        db.session.refresh(workout)
        
        # Format response
        workout_data = format_workout_response(workout)
        
        return jsonify({
            'status': 'success',
            'message': f'Exercise removed from workout',
            'data': workout_data
        }), 200
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error removing exercise from workout: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': f'An error occurred while removing the exercise: {str(e)}'
        }), 500

# Reorder exercises in a workout
@admin_bp.route('/workouts/<int:workout_id>/exercises/reorder', methods=['PUT'])
@admin_required
def reorder_workout_exercises(workout_id):
    """Reorder exercises in a workout based on the provided order"""
    workout = db.session.get(Workout, workout_id) #Workout.query.get(workout_id)
    
    if not workout:
        return jsonify({
            'status': 'error',
            'message': f'Workout with id {workout_id} not found'
        }), 404
    
    data = request.get_json()
    
    if not data or 'exercise_order' not in data:
        return jsonify({
            'status': 'error',
            'message': 'Missing exercise_order in request'
        }), 400
    
    exercise_order = data['exercise_order']
    
    if not isinstance(exercise_order, list):
        return jsonify({
            'status': 'error',
            'message': 'exercise_order must be a list of exercise IDs'
        }), 400
    
    # Get all workout exercises for this workout
    workout_exercises = {we.exercise_id: we for we in workout.workout_exercises}
    
    # Validate that all specified exercises exist in the workout
    missing_exercises = [ex_id for ex_id in exercise_order if ex_id not in workout_exercises]
    if missing_exercises:
        return jsonify({
            'status': 'error',
            'message': 'Some specified exercises do not exist in this workout',
            'missing_exercises': missing_exercises
        }), 400
    
    # Validate that all workout exercises are included in the order
    extra_exercises = [ex_id for ex_id in workout_exercises if ex_id not in exercise_order]
    if extra_exercises:
        return jsonify({
            'status': 'error',
            'message': 'All workout exercises must be included in the reordering',
            'missing_from_order': extra_exercises
        }), 400
    
    try:
        # Update positions based on the order
        for pos, exercise_id in enumerate(exercise_order, 1):
            workout_exercises[exercise_id].position = pos
        
        db.session.commit()
        
        # Refresh the workout to get updated exercise list
        db.session.refresh(workout)
        
        # Format response
        workout_data = format_workout_response(workout)
        
        return jsonify({
            'status': 'success',
            'message': 'Workout exercises reordered successfully',
            'data': workout_data
        }), 200
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f'Error reordering workout exercises: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': f'An error occurred while reordering exercises: {str(e)}'
        }), 500

@admin_bp.route('/workouts', methods=['GET'])
def get_public_workouts():
    """Get all publicly available workouts with optional filtering."""
    # Extract filter parameters from request
    filters = {}
    
    # Add filter parameters if they exist in the query string
    if 'category' in request.args:
        filters['category'] = request.args.get('category')
    
    if 'difficulty_level' in request.args:
        filters['difficulty_level'] = request.args.get('difficulty_level')
    
    if 'duration' in request.args:
        filters['duration'] = request.args.get('duration')
    
    if 'search' in request.args:
        filters['search'] = request.args.get('search')
    
    # Get filtered workouts
    workouts = workout_service.get_public_workouts(filters)
    
    # Prepare response with essential metadata
    response = []
    for workout in workouts:
        # Extract only the necessary fields for the public listing
        response.append({
            'id': workout.id,
            'title': workout.title,
            'description': workout.description,
            'difficulty_level': workout.difficulty_level,
            'duration': workout.duration,  # in minutes
            'category': workout.category,
            'image_url': workout.image_url
        })
    
    return jsonify(response), 200
