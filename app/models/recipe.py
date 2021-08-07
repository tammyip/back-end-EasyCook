from app import db
from flask import current_app

class Recipe(db.Model):
    recipe_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=True)
    # plan_id = db.Column(db.Integer, db.ForeignKey('plan.plan_id'), nullable=True)

    def to_json(self):
        return {
            "recipe_id": self.recipe_id,
            "title_id": self.title,
            "user_id": self.user_id,
        }