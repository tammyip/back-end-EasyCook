from app import db
from flask import current_app

class Plan(db.Model):
    plan_id = db.Column(db.Integer, primary_key=True)
    plan_name = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=True)
    # recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.recipe_id'), nullable=True)

    def to_json(self):
        return {
            "plan_id": self.plan_id,
            "plan_name": self.plan_name,
            "user_id": self.user_id,
        }