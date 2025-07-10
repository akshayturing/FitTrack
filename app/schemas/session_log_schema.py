# # from app import ma
# # from app.models.workout_log import WorkoutSession, SetLog
# # from app.models.exercise import Exercise
# # from marshmallow import fields

# # class ExerciseSchema(ma.SQLAlchemyAutoSchema):
# #     """Schema for serializing exercises."""
# #     class Meta:
# #         model = Exercise
# #         include_fk = True

# # class SetLogSchema(ma.SQLAlchemyAutoSchema):
# #     """Schema for serializing set logs."""
# #     class Meta:
# #         model = SetLog
# #         include_fk = True
        
# #     # Add exercise details
# #     exercise = fields.Nested(ExerciseSchema, exclude=('created_at', 'updated_at'))

# # class WorkoutSessionSchema(ma.SQLAlchemyAutoSchema):
# #     """Schema for serializing workout sessions."""
# #     class Meta:
# #         model = WorkoutSession
# #         include_fk = True
        
# #     # Include nested set logs organized by exercise
# #     set_logs = fields.Nested(SetLogSchema, many=True)
    
# #     # Dynamically organize sets by exercise
# #     exercises = fields.Method('get_exercises_with_sets')
    
# #     def get_exercises_with_sets(self, obj):
# #         """Organize set logs by exercise for cleaner hierarchical response."""
# #         exercise_data = {}
        
# #         # Group sets by exercise
# #         for set_log in obj.set_logs:
# #             if set_log.exercise_id not in exercise_data:
# #                 # Include basic exercise info
# #                 if set_log.exercise:
# #                     exercise_data[set_log.exercise_id] = {
# #                         'id': set_log.exercise_id,
# #                         'name': set_log.exercise.name,
# #                         'type': set_log.exercise.type,
# #                         'target_muscles': set_log.exercise.target_muscles,
# #                         'sets': []
# #                     }
# #                 else:
# #                     # Handle case where exercise might have been deleted
# #                     exercise_data[set_log.exercise_id] = {
# #                         'id': set_log.exercise_id,
# #                         'name': 'Unknown Exercise',
# #                         'sets': []
# #                     }
                
# #             # Add the set data
# #             set_data = {
# #                 'id': set_log.id,
# #                 'set_number': set_log.set_number,
# #                 'reps': set_log.reps,
# #                 'weight': set_log.weight,
# #                 'weight_unit': set_log.weight_unit,
# #                 'duration_seconds': set_log.duration_seconds,
# #                 'distance': set_log.distance,
# #                 'distance_unit': set_log.distance_unit,
# #                 'difficulty': set_log.difficulty,
# #                 'notes': set_log.notes
# #             }
            
# #             exercise_data[set_log.exercise_id]['sets'].append(set_data)
        
# #         # Convert to list for proper JSON response
# #         return list(exercise_data.values())


# # # Create schema instances
# # session_log_schema = WorkoutSessionSchema()
# # session_logs_schema = WorkoutSessionSchema(many=True)
# # set_log_schema = SetLogSchema()
# # set_logs_schema = SetLogSchema(many=True)


# from app import ma
# from marshmallow import Schema, fields

# class ExerciseSchema(ma.Schema):
#     """Schema for serializing exercises."""
#     id = fields.Integer(dump_only=True)
#     name = fields.String()
#     type = fields.String()
#     target_muscles = fields.String()
#     default_reps = fields.Integer()
#     default_sets = fields.Integer()
#     created_at = fields.DateTime(dump_only=True)
#     updated_at = fields.DateTime(dump_only=True)

# class SetLogSchema(ma.Schema):
#     """Schema for serializing set logs."""
#     id = fields.Integer(dump_only=True)
#     workout_session_id = fields.Integer()
#     exercise_id = fields.Integer()
#     set_number = fields.Integer()
#     reps = fields.Integer(allow_none=True)
#     weight = fields.Float(allow_none=True)
#     weight_unit = fields.String(allow_none=True)
#     duration_seconds = fields.Integer(allow_none=True)
#     distance = fields.Float(allow_none=True)
#     distance_unit = fields.String(allow_none=True)
#     difficulty = fields.Integer(allow_none=True)
#     notes = fields.String(allow_none=True)
#     created_at = fields.DateTime(dump_only=True)
#     updated_at = fields.DateTime(dump_only=True)
    
#     # Add exercise details
#     exercise = fields.Nested(ExerciseSchema, exclude=('created_at', 'updated_at'))

# class WorkoutSessionSchema(ma.Schema):
#     """Schema for serializing workout sessions."""
#     id = fields.Integer(dump_only=True)
#     user_id = fields.Integer()
#     workout_assignment_id = fields.Integer(allow_none=True)
#     session_date = fields.DateTime()
#     duration_minutes = fields.Integer(allow_none=True)
#     notes = fields.String(allow_none=True)
#     perceived_exertion = fields.Integer(allow_none=True)
#     completed = fields.Boolean()
#     created_at = fields.DateTime(dump_only=True)
#     updated_at = fields.DateTime(dump_only=True)
    
#     # Include nested set logs organized by exercise
#     set_logs = fields.Nested(SetLogSchema, many=True)
    
#     # Dynamically organize sets by exercise
#     exercises = fields.Method('get_exercises_with_sets')
    
#     def get_exercises_with_sets(self, obj):
#         """Organize set logs by exercise for cleaner hierarchical response."""
#         exercise_data = {}
        
#         # Group sets by exercise
#         for set_log in obj.set_logs:
#             if set_log.exercise_id not in exercise_data:
#                 # Include basic exercise info
#                 if set_log.exercise:
#                     exercise_data[set_log.exercise_id] = {
#                         'id': set_log.exercise_id,
#                         'name': set_log.exercise.name,
#                         'type': set_log.exercise.type,
#                         'target_muscles': set_log.exercise.target_muscles,
#                         'sets': []
#                     }
#                 else:
#                     # Handle case where exercise might have been deleted
#                     exercise_data[set_log.exercise_id] = {
#                         'id': set_log.exercise_id,
#                         'name': 'Unknown Exercise',
#                         'sets': []
#                     }
                
#             # Add the set data
#             set_data = {
#                 'id': set_log.id,
#                 'set_number': set_log.set_number,
#                 'reps': set_log.reps,
#                 'weight': set_log.weight,
#                 'weight_unit': set_log.weight_unit,
#                 'duration_seconds': set_log.duration_seconds,
#                 'distance': set_log.distance,
#                 'distance_unit': set_log.distance_unit,
#                 'difficulty': set_log.difficulty,
#                 'notes': set_log.notes
#             }
            
#             exercise_data[set_log.exercise_id]['sets'].append(set_data)
        
#         # Convert to list for proper JSON response
#         return list(exercise_data.values())


# # Create schema instances
# session_log_schema = WorkoutSessionSchema()
# session_logs_schema = WorkoutSessionSchema(many=True)
# set_log_schema = SetLogSchema()
# set_logs_schema = SetLogSchema(many=True)
from app import ma
from app.models.workout_log import WorkoutSession, SetLog
from app.models.exercise import Exercise
from marshmallow import fields, post_dump

class ExerciseSchema(ma.Schema):
    """Schema for serializing exercises."""
    id = fields.Integer(dump_only=True)
    name = fields.String()
    type = fields.String()
    target_muscles = fields.String()
    default_sets = fields.Integer()
    default_reps = fields.Integer()

class SetLogSchema(ma.Schema):
    """Schema for serializing set logs."""
    id = fields.Integer(dump_only=True)
    workout_session_id = fields.Integer()
    exercise_id = fields.Integer()
    set_number = fields.Integer()
    reps = fields.Integer(allow_none=True)
    weight = fields.Float(allow_none=True)
    weight_unit = fields.String(allow_none=True)
    duration_seconds = fields.Integer(allow_none=True)
    distance = fields.Float(allow_none=True)
    distance_unit = fields.String(allow_none=True)
    difficulty = fields.Integer(allow_none=True)
    notes = fields.String(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

class WorkoutSessionSchema(ma.Schema):
    """Schema for serializing workout sessions."""
    id = fields.Integer(dump_only=True)
    user_id = fields.Integer()
    workout_assignment_id = fields.Integer(allow_none=True)
    session_date = fields.DateTime()
    duration_minutes = fields.Integer(allow_none=True)
    notes = fields.String(allow_none=True)
    perceived_exertion = fields.Integer(allow_none=True)
    completed = fields.Boolean()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    # We'll directly calculate the exercises to avoid lazy loading
    exercises = fields.Method('get_exercises_with_sets')
    
    def get_exercises_with_sets(self, obj):
        """Organize set logs by exercise for cleaner hierarchical response.
        This implementation avoids lazy loading by using the already loaded set_logs."""
        exercise_data = {}
        
        # Ensure set_logs is loaded
        if not hasattr(obj, 'set_logs') or obj.set_logs is None:
            return []
            
        # Group sets by exercise
        for set_log in obj.set_logs:
            if set_log.exercise_id not in exercise_data:
                # Include basic exercise info if we have access to the exercise
                if hasattr(set_log, 'exercise') and set_log.exercise is not None:
                    exercise_data[set_log.exercise_id] = {
                        'id': set_log.exercise_id,
                        'name': set_log.exercise.name,
                        'type': getattr(set_log.exercise, 'type', 'unknown'),
                        'target_muscles': getattr(set_log.exercise, 'target_muscles', ''),
                        'sets': []
                    }
                else:
                    # Handle case where exercise might have been deleted or not loaded
                    exercise_data[set_log.exercise_id] = {
                        'id': set_log.exercise_id,
                        'name': 'Unknown Exercise',
                        'type': 'unknown',
                        'target_muscles': '',
                        'sets': []
                    }
                
            # Add the set data
            set_data = {
                'id': set_log.id,
                'set_number': set_log.set_number,
                'reps': set_log.reps,
                'weight': set_log.weight,
                'weight_unit': set_log.weight_unit,
                'duration_seconds': set_log.duration_seconds,
                'distance': set_log.distance,
                'distance_unit': set_log.distance_unit,
                'difficulty': set_log.difficulty,
                'notes': set_log.notes
            }
            
            exercise_data[set_log.exercise_id]['sets'].append(set_data)
        
        # Convert to list for proper JSON response
        return list(exercise_data.values())


# Create schema instances
session_log_schema = WorkoutSessionSchema()
session_logs_schema = WorkoutSessionSchema(many=True)
set_log_schema = SetLogSchema()
set_logs_schema = SetLogSchema(many=True)