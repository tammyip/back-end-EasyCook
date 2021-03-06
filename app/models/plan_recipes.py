from app import db
from flask import current_app

'''
Recipe to Plan is many to many since a recipe can be on multiple plans. 
Should make a join table model (plan_recipes.py) that will have 2 attributes: 
plan_id and recipe_id
'''
# Not using this table for now as I am creating a new copy of recipe when saving in plan vs. favorties
plan = db.Table('plan', 
db.Column('plan_id', db.Integer, db.ForeignKey('plan.id'), primary_key=True),
db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'), primary_key=True)
)