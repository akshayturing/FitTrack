from flask import Blueprint, request, jsonify, g
from app.services.session_log_service import SessionLogService
from app.schemas.session_log_schema import session_log_schema, session_logs_schema
from app import db
from datetime import datetime

session_log_bp = Blueprint('session_log', __name__)
service = SessionLogService()

@session_log_bp.route('', methods=['POST'])
def create_session_log():
    """Create a new workout session log with exercises and sets."""
    data = request.get_json()
    
    # Validate user authentication (assuming you have middleware for this)
    # This would depend on your authentication system
    user_id = g.user.id if hasattr(g, 'user') else data.get('user_id')
    
    if not user_id:
        return jsonify({"error": "User ID is required"}), 400
    
    try:
        session = service.create_session_log(user_id, data)
        return jsonify({
            "message": "Workout session logged successfully",
            "session": session_log_schema.dump(session)
        }), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to log workout session: {str(e)}"}), 500


@session_log_bp.route('', methods=['GET'])
def get_session_logs():
    """
    Get workout session logs with optional filtering.
    
    Query parameters:
    - user_id: Filter by user ID
    - start_date: Filter sessions after this date (format: YYYY-MM-DD)
    - end_date: Filter sessions before this date (format: YYYY-MM-DD)
    - workout_id: Filter by workout ID
    - assignment_id: Filter by workout assignment ID
    - completed: Filter by completion status (true/false)
    - page: Page number for pagination (default: 1)
    - per_page: Items per page (default: 10)
    """
    # Parse query parameters
    filters = {}
    
    # User authentication check - if user is logged in, default to their ID
    if hasattr(g, 'user'):
        user_id = request.args.get('user_id', g.user.id)
    else:
        user_id = request.args.get('user_id')
        
    if user_id:
        filters['user_id'] = int(user_id)
    
    # Date range filtering
    if request.args.get('start_date'):
        try:
            filters['start_date'] = datetime.strptime(request.args.get('start_date'), '%Y-%m-%d')
        except ValueError:
            return jsonify({"error": "Invalid start_date format. Use YYYY-MM-DD"}), 400
            
    if request.args.get('end_date'):
        try:
            filters['end_date'] = datetime.strptime(request.args.get('end_date'), '%Y-%m-%d')
        except ValueError:
            return jsonify({"error": "Invalid end_date format. Use YYYY-MM-DD"}), 400
    
    # Other filters
    if request.args.get('workout_id'):
        filters['workout_id'] = int(request.args.get('workout_id'))
        
    if request.args.get('assignment_id'):
        filters['workout_assignment_id'] = int(request.args.get('assignment_id'))
        
    if request.args.get('completed') is not None:
        filters['completed'] = request.args.get('completed').lower() == 'true'
    
    # Pagination
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    
    try:
        result = service.get_session_logs(filters, page, per_page)
        return jsonify({
            "sessions": result['items'],
            "pagination": {
                "total": result['total'],
                "pages": result['pages'],
                "current_page": result['page'],
                "per_page": per_page
            }
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to retrieve workout sessions: {str(e)}"}), 500


@session_log_bp.route('/<int:session_id>', methods=['GET'])
def get_session_log(session_id):
    """Get detailed information for a specific workout session log."""
    try:
        session = service.get_session_log_by_id(session_id)
        if not session:
            return jsonify({"error": "Workout session not found"}), 404
            
        # Check if user has permission to view this session
        # This would depend on your authentication system
        if hasattr(g, 'user') and session.user_id != g.user.id:
            # Optional: Allow admin users or trainers to view
            if not hasattr(g, 'user') or not g.user.is_admin:
                return jsonify({"error": "You don't have permission to view this session"}), 403
            
        return jsonify(session_log_schema.dump(session)), 200
    except Exception as e:
        return jsonify({"error": f"Failed to retrieve workout session: {str(e)}"}), 500


@session_log_bp.route('/<int:session_id>', methods=['PUT', 'PATCH'])
def update_session_log(session_id):
    """Update an existing workout session log."""
    data = request.get_json()
    
    try:
        session = service.get_session_log_by_id(session_id)
        if not session:
            return jsonify({"error": "Workout session not found"}), 404
            
        # Check if user has permission to update this session
        if hasattr(g, 'user') and session.user_id != g.user.id:
            # Optional: Allow admin users or trainers to update
            if not hasattr(g, 'user') or not g.user.is_admin:
                return jsonify({"error": "You don't have permission to update this session"}), 403
        
        updated_session = service.update_session_log(session_id, data)
        return jsonify({
            "message": "Workout session updated successfully",
            "session": session_log_schema.dump(updated_session)
        }), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to update workout session: {str(e)}"}), 500


@session_log_bp.route('/<int:session_id>', methods=['DELETE'])
def delete_session_log(session_id):
    """Delete a workout session log."""
    try:
        session = service.get_session_log_by_id(session_id)
        if not session:
            return jsonify({"error": "Workout session not found"}), 404
            
        # Check if user has permission to delete this session
        if hasattr(g, 'user') and session.user_id != g.user.id:
            # Optional: Allow admin users or trainers to delete
            if not hasattr(g, 'user') or not g.user.is_admin:
                return jsonify({"error": "You don't have permission to delete this session"}), 403
        
        service.delete_session_log(session_id)
        return jsonify({
            "message": "Workout session deleted successfully"
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to delete workout session: {str(e)}"}), 500