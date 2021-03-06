from app import db
from flask import current_app

class Plan(db.Model):
    plan_id = db.Column(db.Integer, primary_key=True)
    plan_name = db.Column(db.String)
    # a foreign key column refers to the primary key of the other table
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=True)
    recipes = db.relationship("Recipe", backref="plan", lazy=True)

    def to_json(self):
        return {
            "plan_id": self.plan_id,
            "plan_name": self.plan_name,
            "user_id": self.user_id,
        }