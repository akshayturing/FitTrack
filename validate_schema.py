#!/usr/bin/env python3
"""
Schema validation script for FitTrack database models.

This script verifies:
1. All model relationships function correctly
2. Constraints are properly enforced (uniqueness, not null, etc.)
3. Indexes exist and are properly configured
4. Foreign key relationships function as expected
5. Cascade behaviors work correctly

Run with: python validate_schema.py
"""

import os
import sys
import unittest
import datetime
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import inspect

# Set the Flask environment to testing
os.environ['FLASK_ENV'] = 'testing'
os.environ['FLASK_CONFIG'] = 'testing'

# Import the Flask app and models
from app import create_app, db
from app.models import (User, Workout, Exercise, WorkoutExercise, WorkoutAssignment,
                       WorkoutSession, SetLog, NutritionProfile, NutritionLog, MealLog)


class SchemaValidationTestCase(unittest.TestCase):
    """Test case for validating database schema."""
    
    def setUp(self):
        """Set up test environment."""
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
        print("\n\n=============== SCHEMA VALIDATION TESTS ===============")
    
    def tearDown(self):
        """Clean up after tests."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def print_test_header(self, message):
        """Print a formatted header for each test section."""
        print(f"\n\n{'=' * 20} {message} {'=' * 20}")
    
    def test_01_inspect_tables(self):
        """Inspect all tables to verify they exist with correct columns."""
        self.print_test_header("INSPECTING DATABASE TABLES")
        
        inspector = inspect(db.engine)
        
        # Get all table names
        table_names = inspector.get_table_names()
        print(f"Found {len(table_names)} tables in the database:")
        for table in table_names:
            print(f"  - {table}")
        
        expected_tables = [
            'users', 'workouts', 'exercises', 'workout_exercises', 
            'workout_assignments', 'workout_sessions', 'set_logs',
            'nutrition_profiles', 'nutrition_logs', 'meal_logs'
        ]
        
        # Verify all expected tables exist
        for table in expected_tables:
            self.assertIn(table, table_names)
            
        # Verify key columns in each table
        for table in expected_tables:
            columns = inspector.get_columns(table)
            print(f"\n{table} table has {len(columns)} columns:")
            
            # Print columns and their types
            for column in columns:
                print(f"  - {column['name']}: {column['type']}")
    
    def test_02_inspect_indexes(self):
        """Inspect indexes on all tables."""
        self.print_test_header("INSPECTING DATABASE INDEXES")
        
        inspector = inspect(db.engine)
        
        table_names = inspector.get_table_names()
        
        for table in table_names:
            indexes = inspector.get_indexes(table)
            unique_constraints = inspector.get_unique_constraints(table)
            foreign_keys = inspector.get_foreign_keys(table)
            
            print(f"\nIndexes for {table} table:")
            for index in indexes:
                print(f"  - {index['name']}: columns={index['column_names']}, unique={index.get('unique', False)}")
            
            print(f"Unique constraints for {table} table:")
            for constraint in unique_constraints:
                print(f"  - {constraint.get('name')}: columns={constraint['column_names']}")
                
            print(f"Foreign keys for {table} table:")
            for fk in foreign_keys:
                print(f"  - {fk.get('name')}: {fk['constrained_columns']} -> {fk['referred_table']}.{fk['referred_columns']}")
    
    def test_03_user_model_constraints(self):
        """Test User model constraints."""
        self.print_test_header("TESTING USER MODEL CONSTRAINTS")
        
        # Create a valid user
        user1 = User(
            name="Test User",
            username="testuser",
            email="test@example.com",
            password="password123"
        )
        db.session.add(user1)
        db.session.commit()
        print("Created first user successfully")
        
        # Test unique username constraint
        user2 = User(
            name="Another User",
            username="testuser",  # Same username as user1
            email="different@example.com",
            password="password123"
        )
        db.session.add(user2)
        try:
            db.session.commit()
            self.fail("Should have raised IntegrityError for duplicate username")
        except IntegrityError:
            print("✓ Unique username constraint works correctly")
            db.session.rollback()
        
        # Test unique email constraint
        user3 = User(
            name="Third User",
            username="testuser3",
            email="test@example.com",  # Same email as user1
            password="password123"
        )
        db.session.add(user3)
        try:
            db.session.commit()
            self.fail("Should have raised IntegrityError for duplicate email")
        except IntegrityError:
            print("✓ Unique email constraint works correctly")
            db.session.rollback()
        
        # Test not null constraints
        user4 = User(
            name="Fourth User",
            # username is missing (should be not null)
            email="fourth@example.com",
            password="password123"
        )
        db.session.add(user4)
        try:
            db.session.commit()
            self.fail("Should have raised IntegrityError for null username")
        except IntegrityError:
            print("✓ Not null username constraint works correctly")
            db.session.rollback()
    
    def test_04_relationship_workout_exercise(self):
        """Test Workout to Exercise relationship through WorkoutExercise."""
        self.print_test_header("TESTING WORKOUT-EXERCISE RELATIONSHIPS")
        
        # Create user
        user = User(
            name="Test User",
            username="testuser",
            email="test@example.com",
            password="password123"
        )
        db.session.add(user)
        db.session.commit()
        
        # Create workout
        workout = Workout(
            title="Upper Body Workout",
            description="Focus on chest, shoulders, and triceps",
            category="Strength",
            created_by=user.id
        )
        db.session.add(workout)
        
        # Create exercises
        exercises = [
            Exercise(name="Bench Press", muscle_group="Chest", default_sets=3, default_reps=10),
            Exercise(name="Shoulder Press", muscle_group="Shoulders", default_sets=3, default_reps=10),
            Exercise(name="Tricep Extension", muscle_group="Triceps", default_sets=3, default_reps=12)
        ]
        for ex in exercises:
            db.session.add(ex)
        
        db.session.commit()
        print(f"Created workout and {len(exercises)} exercises")
        
        # Associate exercises with workout
        workout_exercises = []
        for i, ex in enumerate(exercises, 1):
            we = WorkoutExercise(
                workout_id=workout.id,
                exercise_id=ex.id,
                order_index=i,
                sets=ex.default_sets,
                reps=str(ex.default_reps),
                rest_seconds=60
            )
            workout_exercises.append(we)
            db.session.add(we)
        
        db.session.commit()
        print(f"Associated {len(workout_exercises)} exercises with the workout")
        
        # Verify relationships
        # 1. From workout to exercises
        workout_exs = workout.exercises.all()
        self.assertEqual(len(workout_exs), 3)
        print(f"✓ Workout correctly has {len(workout_exs)} associated exercises")
        
        # 2. From exercise to workouts
        ex_workouts = exercises[0].workouts.all()
        self.assertEqual(len(ex_workouts), 1)
        print(f"✓ Exercise correctly has {len(ex_workouts)} associated workouts")
        
        # 3. Test order_index works correctly
        ordered_exs = workout.exercises.order_by(WorkoutExercise.order_index).all()
        for i, we in enumerate(ordered_exs, 1):
            self.assertEqual(we.order_index, i)
        print("✓ Exercise ordering works correctly")
    
    def test_05_workout_assignment_constraints(self):
        """Test WorkoutAssignment model constraints."""
        self.print_test_header("TESTING WORKOUT ASSIGNMENT CONSTRAINTS")
        
        # Create users
        user1 = User(name="User One", username="user1", email="user1@example.com", password="password123")
        user2 = User(name="User Two", username="user2", email="user2@example.com", password="password123")
        coach = User(name="Coach", username="coach", email="coach@example.com", password="password123")
        db.session.add_all([user1, user2, coach])
        
        # Create workouts
        workout1 = Workout(title="Beginner Workout", created_by=coach.id)
        workout2 = Workout(title="Advanced Workout", created_by=coach.id)
        db.session.add_all([workout1, workout2])
        
        db.session.commit()
        print("Created users and workouts for assignment testing")
        
        # Create valid assignment
        assignment1 = WorkoutAssignment(
            user_id=user1.id,
            workout_id=workout1.id,
            assigned_by=coach.id,
            start_date=datetime.date.today()
        )
        db.session.add(assignment1)
        db.session.commit()
        print("Created first workout assignment successfully")
        
        # Test unique constraint on (user_id, workout_id)
        assignment2 = WorkoutAssignment(
            user_id=user1.id,  # Same user
            workout_id=workout1.id,  # Same workout
            assigned_by=coach.id
        )
        db.session.add(assignment2)
        try:
            db.session.commit()
            self.fail("Should have raised IntegrityError for duplicate user-workout assignment")
        except IntegrityError:
            print("✓ Unique user-workout constraint works correctly")
            db.session.rollback()
        
        # Test foreign key constraints
        assignment3 = WorkoutAssignment(
            user_id=999,  # Non-existent user
            workout_id=workout1.id,
            assigned_by=coach.id
        )
        db.session.add(assignment3)
        try:
            db.session.commit()
            self.fail("Should have raised IntegrityError for non-existent user_id")
        except IntegrityError:
            print("✓ Foreign key constraint on user_id works correctly")
            db.session.rollback()
    
    def test_06_nutrition_related_models(self):
        """Test nutrition-related models and relationships."""
        self.print_test_header("TESTING NUTRITION MODELS")
        
        # Create user with nutrition profile
        user = User(
            name="Nutrition Test User",
            username="nutritionuser",
            email="nutrition@example.com",
            password="password123",
            calorie_goal=2000,
            protein_goal=150
        )
        db.session.add(user)
        db.session.commit()
        
        # Create nutrition profile
        profile = NutritionProfile(
            user_id=user.id,
            weight=80.5,
            height=180.0,
            body_fat=15.0,
            calorie_goal=2200,
            protein_goal=160,
            carbs_goal=220,
            fat_goal=70,
            fiber_goal=30,
            water_goal=3000,
            activity_level="moderately_active",
            fitness_goal="muscle_gain"
        )
        db.session.add(profile)
        db.session.commit()
        print("Created user with nutrition profile successfully")
        
        # Test one-to-one relationship
        self.assertEqual(user.nutrition_profile.id, profile.id)
        print("✓ User-NutritionProfile one-to-one relationship works")
        
        # Create nutrition log for today
        today = datetime.date.today()
        nutrition_log = NutritionLog(
            user_id=user.id,
            date=today, 
            total_calories=0,
            total_protein=0
        )
        db.session.add(nutrition_log)
        db.session.commit()
        
        # Add meals to the nutrition log
        meals = [
            MealLog(
                nutrition_log_id=nutrition_log.id,
                meal_type="breakfast",
                name="Oatmeal with protein",
                calories=350,
                protein=25,
                carbs=45,
                fat=8,
                time_consumed=datetime.datetime.now().replace(hour=8, minute=0)
            ),
            MealLog(
                nutrition_log_id=nutrition_log.id,
                meal_type="lunch",
                name="Chicken salad",
                calories=550,
                protein=40,
                carbs=30,
                fat=25,
                time_consumed=datetime.datetime.now().replace(hour=12, minute=30)
            )
        ]
        
        db.session.add_all(meals)
        db.session.commit()
        print(f"Added {len(meals)} meals to nutrition log")
        
        # Test the relationship from nutrition log to meals
        log_meals = nutrition_log.meal_logs.all()
        self.assertEqual(len(log_meals), 2)
        print("✓ NutritionLog-MealLog one-to-many relationship works")
        
        # Test unique constraint on (user_id, date)
        duplicate_log = NutritionLog(
            user_id=user.id,
            date=today  # Same date as existing log
        )
        db.session.add(duplicate_log)
        try:
            db.session.commit()
            self.fail("Should have raised IntegrityError for duplicate date nutrition log")
        except IntegrityError:
            print("✓ Unique user-date constraint works for nutrition logs")
            db.session.rollback()
    
    def test_07_workout_session_and_set_logs(self):
        """Test workout session and set log models and relationships."""
        self.print_test_header("TESTING WORKOUT SESSIONS AND SET LOGS")
        
        # Create user
        user = User(
            name="Session User",
            username="sessionuser",
            email="session@example.com",
            password="password123"
        )
        db.session.add(user)
        
        # Create workout
        workout = Workout(
            title="Full Body Workout",
            description="Complete body workout",
            category="Strength",
            created_by=user.id
        )
        db.session.add(workout)
        
        # Create exercises
        exercises = [
            Exercise(name="Squat", muscle_group="Legs", default_sets=4, default_reps=8),
            Exercise(name="Deadlift", muscle_group="Back", default_sets=3, default_reps=5)
        ]
        for ex in exercises:
            db.session.add(ex)
        
        db.session.commit()
        print("Created user, workout, and exercises for session testing")
        
        # Create workout session
        session = WorkoutSession(
            user_id=user.id,
            workout_id=workout.id,
            started_at=datetime.datetime.now() - datetime.timedelta(hours=1),
            completed_at=datetime.datetime.now(),
            mood="Energetic",
            difficulty_rating=7
        )
        session.update_duration()
        db.session.add(session)
        db.session.commit()
        print("Created workout session successfully")
        
        # Create set logs
        set_logs = []
        # For first exercise
        for i in range(1, 5):  # 4 sets
            set_logs.append(SetLog(
                session_id=session.id,
                exercise_id=exercises[0].id,
                set_number=i,
                reps=8,
                weight=100 + (i*5),  # Increasing weight
                rpe=7.5,
                completed=True
            ))
        
        # For second exercise
        for i in range(1, 4):  # 3 sets
            set_logs.append(SetLog(
                session_id=session.id,
                exercise_id=exercises[1].id,
                set_number=i,
                reps=5,
                weight=150 + (i*10),  # Increasing weight
                rpe=8.0,
                completed=True
            ))
        
        db.session.add_all(set_logs)
        db.session.commit()
        print(f"Added {len(set_logs)} set logs to session")
        
        # Test session to set logs relationship
        session_sets = session.set_logs.all()
        self.assertEqual(len(session_sets), 7)
        print("✓ Session-SetLog one-to-many relationship works")
        
        # Test unique constraint on (session_id, exercise_id, set_number)
        duplicate_set = SetLog(
            session_id=session.id,
            exercise_id=exercises[0].id,
            set_number=1,  # Duplicate of first set
            reps=8,
            weight=100
        )
        db.session.add(duplicate_set)
        try:
            db.session.commit()
            self.fail("Should have raised IntegrityError for duplicate set number")
        except IntegrityError:
            print("✓ Unique session-exercise-set constraint works")
            db.session.rollback()
    
    def test_08_cascade_delete_behavior(self):
        """Test cascade delete behavior for related models."""
        self.print_test_header("TESTING CASCADE DELETE BEHAVIOR")
        
        # Create test data
        user = User(name="Cascade User", username="cascadeuser", email="cascade@example.com", password="password123")
        db.session.add(user)
        
        # Create nutrition profile
        profile = NutritionProfile(
            user_id=user.id,
            calorie_goal=2000,
            protein_goal=150
        )
        db.session.add(profile)
        
        # Create workout
        workout = Workout(title="Test Workout", created_by=user.id)
        db.session.add(workout)
        db.session.commit()
        
        # Create workout session
        session = WorkoutSession(
            user_id=user.id,
            workout_id=workout.id,
            started_at=datetime.datetime.now()
        )
        db.session.add(session)
        
        # Create exercise
        exercise = Exercise(name="Test Exercise", muscle_group="Test")
        db.session.add(exercise)
        db.session.commit()
        
        # Create set log
        set_log = SetLog(
            session_id=session.id,
            exercise_id=exercise.id,
            set_number=1,
            reps=10,
            weight=100
        )
        db.session.add(set_log)
        
        # Create nutrition log
        nutrition_log = NutritionLog(
            user_id=user.id,
            date=datetime.date.today()
        )
        db.session.add(nutrition_log)
        
        # Create meal log
        meal_log = MealLog(
            nutrition_log_id=nutrition_log.id,
            meal_type="lunch",
            name="Test Meal",
            calories=500
        )
        db.session.add(meal_log)
        
        db.session.commit()
        
        print("Created test data for cascade delete testing")
        
        # Test 1: Delete session should cascade to set logs
        session_id = session.id
        set_log_id = set_log.id
        db.session.delete(session)
        db.session.commit()
        
        # Verify set log is deleted
        deleted_set_log = SetLog.query.get(set_log_id)
        self.assertIsNone(deleted_set_log)
        print("✓ Deleting session cascades to set logs")
        
        # Test 2: Delete user should cascade to nutrition profile and logs
        user_id = user.id
        profile_id = profile.id
        nutrition_log_id = nutrition_log.id
        meal_log_id = meal_log.id
        
        db.session.delete(user)
        db.session.commit()
        
        # Verify cascaded deletions
        deleted_profile = NutritionProfile.query.get(profile_id)
        deleted_nutrition_log = NutritionLog.query.get(nutrition_log_id)
        deleted_meal_log = MealLog.query.get(meal_log_id)
        
        self.assertIsNone(deleted_profile)
        self.assertIsNone(deleted_nutrition_log)
        self.assertIsNone(deleted_meal_log)
        
        print("✓ Deleting user cascades to nutrition profile and logs")

    def test_09_not_null_constraints(self):
        """Test that not null constraints are enforced."""
        self.print_test_header("TESTING NOT NULL CONSTRAINTS")
        
        # Test WorkoutSession with null user_id
        session = WorkoutSession(
            # Missing user_id
            workout_id=1,
            started_at=datetime.datetime.now()
        )
        db.session.add(session)
        try:
            db.session.commit()
            self.fail("Should have raised IntegrityError for null user_id")
        except IntegrityError:
            print("✓ Not null constraint on WorkoutSession.user_id works")
            db.session.rollback()
        
        # Test Exercise with null name
        exercise = Exercise(
            # Missing name
            muscle_group="Test"
        )
        db.session.add(exercise)
        try:
            db.session.commit()
            self.fail("Should have raised IntegrityError for null exercise name")
        except IntegrityError:
            print("✓ Not null constraint on Exercise.name works")
            db.session.rollback()
        
        # Test MealLog with null meal_type
        log = NutritionLog(user_id=1, date=datetime.date.today())
        db.session.add(log)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            
        # Create a valid log first
        user = User(name="Test", username="test99", email="test99@example.com", password="password")
        db.session.add(user)
        db.session.commit()
        
        log = NutritionLog(user_id=user.id, date=datetime.date.today())
        db.session.add(log)
        db.session.commit()
        
        meal = MealLog(
            nutrition_log_id=log.id,
            # Missing meal_type
            name="Test Meal",
            calories=500
        )
        db.session.add(meal)
        try:
            db.session.commit()
            self.fail("Should have raised IntegrityError for null meal_type")
        except IntegrityError:
            print("✓ Not null constraint on MealLog.meal_type works")
            db.session.rollback()


if __name__ == "__main__":
    unittest.main(verbosity=2)