# app/models/nutrition_goal.py
from app import db
from datetime import datetime

class NutritionGoal(db.Model):
    __tablename__ = 'nutrition_goals'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    daily_calories = db.Column(db.Integer, nullable=True)
    protein_grams = db.Column(db.Integer, nullable=True)
    carbs_grams = db.Column(db.Integer, nullable=True)
    fat_grams = db.Column(db.Integer, nullable=True)
    fiber_grams = db.Column(db.Integer, nullable=True)
    water_ml = db.Column(db.Integer, nullable=True)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def is_active(self):
        """Check if the nutrition goal is currently active."""
        now = datetime.utcnow()
        if self.end_date:
            return self.start_date <= now <= self.end_date
        return self.start_date <= now
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'daily_calories': self.daily_calories,
            'protein_grams': self.protein_grams,
            'carbs_grams': self.carbs_grams,
            'fat_grams': self.fat_grams,
            'fiber_grams': self.fiber_grams,
            'water_ml': self.water_ml,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_active': self.is_active()
        }
    
    def __repr__(self):
        return f"<NutritionGoal {self.id} for User {self.user_id}>"