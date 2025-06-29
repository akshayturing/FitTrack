# app/models/meal_log.py
from app import db
from datetime import datetime

class MealLog(db.Model):
    __tablename__ = 'meal_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    nutrition_log_id = db.Column(db.Integer, db.ForeignKey('nutrition_logs.id', ondelete='CASCADE'), nullable=False, index=True)
    meal_type = db.Column(db.String(50), nullable=False, index=True)  # breakfast, lunch, dinner, snack
    name = db.Column(db.String(100), nullable=False)
    calories = db.Column(db.Integer, nullable=False, default=0)
    protein = db.Column(db.Float, nullable=True)  # in grams
    carbs = db.Column(db.Float, nullable=True)    # in grams
    fat = db.Column(db.Float, nullable=True)      # in grams
    fiber = db.Column(db.Float, nullable=True)    # in grams
    sugar = db.Column(db.Float, nullable=True)    # in grams
    sodium = db.Column(db.Float, nullable=True)   # in mg
    serving_size = db.Column(db.String(50), nullable=True)
    servings = db.Column(db.Float, nullable=False, default=1.0)
    time_consumed = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    notes = db.Column(db.Text, nullable=True)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    __table_args__ = (
        # Index for meal type analysis
        db.Index('idx_meal_type_time', 'meal_type', 'time_consumed'),
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'nutrition_log_id': self.nutrition_log_id,
            'meal_type': self.meal_type,
            'name': self.name,
            'calories': self.calories,
            'protein': self.protein,
            'carbs': self.carbs,
            'fat': self.fat,
            'fiber': self.fiber,
            'sugar': self.sugar,
            'sodium': self.sodium,
            'serving_size': self.serving_size,
            'servings': self.servings,
            'time_consumed': self.time_consumed.isoformat() if self.time_consumed else None,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f"<MealLog {self.id}: {self.meal_type} - {self.name}>"