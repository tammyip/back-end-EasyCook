from flask import Blueprint, request, jsonify, make_response
# from flask import Flask, session
# from flask_session import Session
from app import db
from app.models import recipe
from app.models.user import User
from app.models.recipe import Recipe
from app.models.plan import Plan
# from sqlalchemy.sql import exists

user_bp = Blueprint("user", __name__, url_prefix="/user")
recipe_bp = Blueprint("recipes", __name__, url_prefix="/recipes")
plan_bp = Blueprint("plans", __name__, url_prefix="/plans")

# USERS
################################################################
# View all users
@user_bp.route("", methods=["GET"], strict_slashes=False)
def view_users():
    users=User.query.all()
    view_users=[user.to_json() for user in users if users]
    return jsonify(view_users), 200

# Create an user
@user_bp.route("", methods=["POST"], strict_slashes=False)
def create_user():
    request_body = request.get_json()
    if ("name" not in request_body 
        or "email" not in request_body): 
        return jsonify(details = f'Invalid data'), 400

    # if session.query(User.query.filter(User.id == 1).exists()).scalar() is None:
    user = User.query.filter_by(email=request_body["email"]).first()
    status_code = 400
    if user:
        # if it's an existing user, just return status_code 200, no adding to database
        status_code = 200
    else:
        user = User(name=request_body["name"],
                        email=request_body["email"])  
        db.session.add(user)
        db.session.commit()
        # if it's a new user, return status_code 201
        status_code =201
    return jsonify(user_id=user.user_id, name=user.name, email=user.email), status_code

# FAVORITES
################################################################
# Add a recipe to Favorites
@user_bp.route("/<user_id>/favorites", methods=["POST"], strict_slashes=False)
def add_recipe_to_user(user_id):
    request_body = request.get_json()
    if ("label" not in request_body
        or "image" not in request_body
        or "url" not in request_body):  
        return jsonify(details = f'Invalid data'), 400
    
    recipe = Recipe.query.filter_by(url=request_body["url"]).first()

    if recipe:
        return jsonify(details = f'recipe already in Favorites')
    else:
        new_recipe_in_user = Recipe(title=request_body["label"],
                                    image=request_body["image"],
                                    url=request_body["url"],
                                    user_id=user_id)

        db.session.add(new_recipe_in_user)
        db.session.commit()

    return jsonify(new_recipe_in_user.to_json()), 200

# Delete a recipe in Favorites
@recipe_bp.route("/<recipe_id>", methods=["DELETE"], strict_slashes=False)
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    db.session.delete(recipe)
    db.session.commit()
    return jsonify(recipe = f'Recipe {recipe.recipe_id} "{recipe.title}" successfully deleted')

# View all recipes saved in Favorites by an user
@user_bp.route("/<user_id>/favorites", methods=["GET"], strict_slashes=False)
def view_recipes_in_favorites(user_id):

    user = User.query.get_or_404(user_id)

    recipes = user.recipes # [{}, {}, {}]
    recipes_in_favorites = [recipe.to_json() for recipe in recipes if recipes]
    return jsonify(recipes=recipes_in_favorites)

# Delete all recipes saved in Favorites by an user
@recipe_bp.route("", methods=["DELETE"], strict_slashes=False)
def delete_all_recipes():
    recipes = Recipe.query.all()
    for recipe in recipes:
        db.session.delete(recipe)
    db.session.commit()
    return jsonify(board = f'All recipes successfully deleted in favorite'), 200

# PLAN
################################################################
# View all plans in database
@plan_bp.route("", methods=["GET"], strict_slashes=False)
def view_all_plans_in_db():
    plans=Plan.query.all()
    view_plans=[plan.to_json() for plan in plans if plans]
    return jsonify(view_plans), 200

# Add a plan for an user
@user_bp.route("/<user_id>/plans", methods=["POST"], strict_slashes=False)
def add_plan_to_user(user_id):
    request_body = request.get_json()
    if ("plan_name" not in request_body): 
        return jsonify(details = f'Invalid data'), 400  

    new_plan_in_user = Plan(plan_name=request_body["plan_name"],
                            user_id=user_id)  
    db.session.add(new_plan_in_user)
    db.session.commit()
    return jsonify(new_plan_in_user.to_json()), 200

### View all plans by an user ###
@user_bp.route("/<user_id>/plans", methods=["GET"], strict_slashes=False)
def view_plans_in_user(user_id):

    user = User.query.get_or_404(user_id)

    plans = user.plans # [{}, {}, {}]
    plans_in_user = [plan.to_json() for plan in plans if plans]
    return jsonify(plans=plans_in_user)

# Add a recipe to a Plan
@plan_bp.route("/<plan_id>", methods=["POST"], strict_slashes=False)
def add_recipe_to_plan(plan_id):
    request_body = request.get_json()
    if ("label" not in request_body
    or "image" not in request_body
    or "url" not in request_body):  
        return jsonify(details = f'Invalid data'), 400

    new_recipe_in_plan = Recipe(title=request_body["label"],
                                image=request_body["image"],
                                url=request_body["url"],
                                plan_id=plan_id
                                )

    db.session.add(new_recipe_in_plan)
    db.session.commit()
    return jsonify(new_recipe_in_plan.to_json()), 200

# View all recipes saved in a plan
@plan_bp.route("/<plan_id>/recipes", methods=["GET"], strict_slashes=False)
def view_recipes_in_plans(plan_id):

    plan = Plan.query.get_or_404(plan_id)

    recipes = plan.recipes # [{}, {}, {}]
    recipes_in_plans = [recipe.to_json() for recipe in recipes if recipes]
    return jsonify(recipes=recipes_in_plans)

# Delete a recipe in a plan
@recipe_bp.route("/<recipe_id>", methods=["DELETE"], strict_slashes=False)
def delete_card(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    db.session.delete(recipe)
    db.session.commit()
    return jsonify(card = f'Recipe {recipe.recipe_id} "{recipe.title}" successfully deleted')

# Delete a plan
@plan_bp.route("/<plan_id>", methods=["DELETE"], strict_slashes=False)
def delete_a_plan(plan_id):
    plan = Plan.query.get_or_404(plan_id)
    recipes = Recipe.query.filter_by(plan_id=int(plan_id))
    for recipe in recipes:
        db.session.delete(recipe)
    db.session.delete(plan)
    db.session.commit()
    return jsonify(recipe = f'Plan {plan.plan_id} "{plan.plan_name}" successfully deleted')