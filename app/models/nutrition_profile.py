# app/models/nutrition_profile.py
from app import db
from datetime import datetime

class NutritionProfile(db.Model):
    __tablename__ = 'nutrition_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True, index=True)
    
    # Basic metrics
    weight = db.Column(db.Float, nullable=True)  # in kg
    height = db.Column(db.Float, nullable=True)  # in cm
    body_fat = db.Column(db.Float, nullable=True)  # percentage
    bmr = db.Column(db.Integer, nullable=True)  # Basal Metabolic Rate
    tdee = db.Column(db.Integer, nullable=True)  # Total Daily Energy Expenditure
    
    # Goal related
    weight_goal = db.Column(db.Float, nullable=True)  # Target weight in kg
    activity_level = db.Column(db.String(20), nullable=True)  # sedentary, lightly_active, moderately_active, very_active, extremely_active
    fitness_goal = db.Column(db.String(20), nullable=True)  # weight_loss, maintenance, muscle_gain
    
    # Macronutrients
    calorie_goal = db.Column(db.Integer, nullable=True)  
    protein_goal = db.Column(db.Integer, nullable=True)  # in grams
    carbs_goal = db.Column(db.Integer, nullable=True)    # in grams
    fat_goal = db.Column(db.Integer, nullable=True)      # in grams
    fiber_goal = db.Column(db.Integer, nullable=True)    # in grams  
    
    # Hydration
    water_goal = db.Column(db.Integer, nullable=True)    # in mL
    
    # Dietary preferences
    dietary_restrictions = db.Column(db.String(255), nullable=True)  # comma-separated: vegetarian,vegan,gluten-free,etc
    allergies = db.Column(db.String(255), nullable=True)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'weight': self.weight,
            'height': self.height,
            'body_fat': self.body_fat,
            'bmr': self.bmr,
            'tdee': self.tdee,
            'weight_goal': self.weight_goal,
            'activity_level': self.activity_level,
            'fitness_goal': self.fitness_goal,
            'calorie_goal': self.calorie_goal,
            'protein_goal': self.protein_goal,
            'carbs_goal': self.carbs_goal,
            'fat_goal': self.fat_goal,
            'fiber_goal': self.fiber_goal,
            'water_goal': self.water_goal,
            'dietary_restrictions': self.dietary_restrictions,
            'allergies': self.allergies,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        return f"<NutritionProfile for User {self.user_id}>"