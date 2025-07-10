# app/models/nutrition_log.py
from app import db
from datetime import datetime

class NutritionLog(db.Model):
    __tablename__ = 'nutrition_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    date = db.Column(db.Date, nullable=False, default=datetime.utcnow().date)
    
    # Daily totals
    total_calories = db.Column(db.Integer, default=0)
    total_protein = db.Column(db.Float, default=0)  # in grams
    total_carbs = db.Column(db.Float, default=0)    # in grams
    total_fat = db.Column(db.Float, default=0)      # in grams
    total_fiber = db.Column(db.Float, default=0)    # in grams
    total_sugar = db.Column(db.Float, default=0)    # in grams
    total_sodium = db.Column(db.Float, default=0)   # in mg
    total_water = db.Column(db.Integer, default=0)  # in mL
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    meal_logs = db.relationship('MealLog', backref='nutrition_log', lazy='dynamic', cascade='all, delete-orphan')
    
    __table_args__ = (
        db.UniqueConstraint('user_id', 'date', name='uix_user_date_nutrition'),
        db.Index('idx_nutrition_user_date', 'user_id', 'date'),
    )
    
    def to_dict(self, include_meals=False):
        result = {
            'id': self.id,
            'user_id': self.user_id,
            'date': self.date.isoformat() if self.date else None,
            'total_calories': self.total_calories,
            'total_protein': self.total_protein,
            'total_carbs': self.total_carbs,
            'total_fat': self.total_fat,
            'total_fiber': self.total_fiber,
            'total_sugar': self.total_sugar,
            'total_sodium': self.total_sodium,
            'total_water': self.total_water,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_meals:
            result['meals'] = [meal.to_dict() for meal in self.meal_logs]
            
        return result
    
    def __repr__(self):
        return f"<NutritionLog {self.id}: User {self.user_id} on {self.date}>"