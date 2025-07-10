from flask import Blueprint, render_template, jsonify, abort, current_app
from flask_login import login_required, current_user
from app.models.workout import Workout
from app.schemas.workout_schema import workouts_schema
from app.services.workout_service import WorkoutService
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.workout_assignment import WorkoutAssignment

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@login_required
def workout_dashboard():
    """Render the workout dashboard page"""
    return render_template('workout_dashboard.html', user=current_user)




# @dashboard_bp.route('/users/<int:user_id>/workouts', methods=['GET'])
# @jwt_required()
# def get_user_workouts_api(user_id):
#     """
#     API endpoint to get all workouts assigned to a user.
#     JWT authenticated version.
#     """
#     # Get user ID from JWT token
#     current_user_id = get_jwt_identity()
    
#     # Check if the user is requesting their own workouts
#     if current_user_id != user_id:
#         return jsonify({"error": "Unauthorized access"}), 403
    
#     try:
#         # Get all workout assignments for the user
#         assignments = WorkoutAssignment.query.filter_by(user_id=user_id, is_active=True).all()
        
#         # Extract workout IDs from assignments
#         workout_ids = [assignment.workout_id for assignment in assignments]
        
#         # Get all relevant workouts
#         workouts = Workout.query.filter(Workout.id.in_(workout_ids)).all() if workout_ids else []
        
#         # Return serialized workouts
#         return jsonify({"workouts": workouts_schema.dump(workouts)}), 200
#     except Exception as e:
#         current_app.logger.error(f"Error fetching user workouts: {str(e)}")
#         return jsonify({"error": "Failed to fetch workouts"}), 500

# @dashboard_bp.route('/users/<int:user_id>/workouts', methods=['GET'])
# @jwt_required()
# def get_user_workouts_api(user_id):
#     """
#     API endpoint to get all workouts assigned to a user.
#     JWT authenticated version.
#     """
#     # Get user ID from JWT token
#     current_user_id = get_jwt_identity()
    
#     try:
#         # Convert IDs to integers for comparison (in case one is a string)
#         current_user_id = int(current_user_id)
#     except (ValueError, TypeError):
#         pass
    
#     try:
#         # First check: Basic authorization - is the requested user ID matching the token?
#         if current_user_id != user_id:
#             # Second check: Is the current user an admin?
#             current_user = User.query.get(current_user_id)
#             if not current_user or not getattr(current_user, 'is_admin', False):
#                 # Log the attempt for security monitoring
#                 current_app.logger.warning(
#                     f"User {current_user_id} attempted unauthorized access to user {user_id}'s workouts"
#                 )
#                 return jsonify({"error": "Unauthorized access. You can only view your own workouts."}), 403
        
#         # Get all workout assignments for the user
#         assignments = WorkoutAssignment.query.filter_by(user_id=user_id, is_active=True).all()
        
#         # Extract workout IDs from assignments
#         workout_ids = [assignment.workout_id for assignment in assignments]
        
#         # Get all relevant workouts
#         workouts = Workout.query.filter(Workout.id.in_(workout_ids)).all() if workout_ids else []
        
#         # Return serialized workouts
#         return jsonify({"workouts": workouts_schema.dump(workouts)}), 200
    
#     except Exception as e:
#         current_app.logger.error(f"Error fetching user workouts: {str(e)}")
#         return jsonify({"error": f"Failed to fetch workouts: {str(e)}"}), 500

# @dashboard_bp.route('/api/users/<i>/workouts')
# @login_required
# def get_user_workouts(user_id):
#     """API endpoint to get all workouts assigned to a user"""
#     # Verify authorization
#     if current_user.id != user_id and not current_user.is_admin:
#         return jsonify({"error": "Unauthorized access"}), 403

#     try:
#         workouts = WorkoutService.get_user_assigned_workouts(user_id)
#         return jsonify({"workouts": workouts_schema.dump(workouts)}), 200
#     except Exception as e:
#         current_app.logger.error(f"Error fetching user workouts: {str(e)}")
#         return jsonify({"error": "Failed to fetch workouts"}), 500
    
@dashboard_bp.route('/workout-session/start/int:workout_id')
@login_required
def start_workout_session(workout_id):
    """Start a new workout session for the specified workout"""
    # Verify workout exists
    workout = Workout.query.get_or_404(workout_id)

    # Verify workout is assigned to user
    if not WorkoutService.is_workout_assigned_to_user(current_user.id, workout_id):
        abort(404, description="Workout not assigned to user or inactive")

    return render_template('workout_session.html', workout=workout)

## 3. Frontend Implementation

### HTML Template Structure (`templates/workout_dashboard.html`):

