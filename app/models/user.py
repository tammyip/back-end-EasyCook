from app import db
from flask import current_app

'''
User to Recipe should be a one to many relationship, it's ok if a recipe is saved twice in the database but with different user_ids. 
We woulnd't want one user deleting a rescipe to affect other users saved recipes.
'''

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    name = db.Column(db.String)
    email = db.Column(db.String)  
    recipes = db.relationship("Recipe", backref="user", lazy=True)
    plans = db.relationship("Plan", backref="user", lazy=True)

    def to_json(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "email": self.email,
        }