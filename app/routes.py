from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.user import User
from app.models.recipe import Recipe
from app.models.plan import Plan
from sqlalchemy.sql import exists

user_bp = Blueprint("user", __name__, url_prefix="/user")
recipe_bp = Blueprint("recipes", __name__, url_prefix="/favorites")
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
    user_count = User.query.filter_by(email=request_body["email"]).count()
    if user_count > 0:
        return "user already in database, cannot be added"
    else:
        new_user = User(name=request_body["name"],
                        email=request_body["email"])  
        db.session.add(new_user)
        db.session.commit()
        return jsonify(user_id=new_user.user_id, name=new_user.name, email=new_user.email), 201

# Add a recipe to Favorites
@user_bp.route("/<user_id>/favorites", methods=["POST"], strict_slashes=False)
def add_recipe_to_user(user_id):
    request_body = request.get_json()
    if ("label" not in request_body
    or "image" not in request_body
    or "url" not in request_body):  
        return jsonify(details = f'Invalid data'), 400

    new_recipe_in_user = Recipe(title=request_body["label"],
                                image=request_body["image"],
                                url=request_body["url"],
                                user_id=user_id)

    db.session.add(new_recipe_in_user)
    db.session.commit()
    return jsonify(new_recipe_in_user.to_json()), 200

# Delete a recipe in Favorites
@user_bp.route("/<user_id>/favorites/<recipe_id>", methods=["DELETE"], strict_slashes=False)
def delete_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    db.session.delete(recipe)
    db.session.commit()
    return jsonify(recipe = f'Recipe {recipe.recipe_id} "{recipe.title}" successfully deleted')

### View all recipes saved in Favorites by an user ###
@user_bp.route("/<user_id>/favorites", methods=["GET"], strict_slashes=False)
def view_recipes_in_favorites(user_id):

    user = User.query.get_or_404(user_id)

    recipes = user.recipes # [{}, {}, {}]
    recipes_in_favorites = [recipe.to_json() for recipe in recipes if recipes]
    return jsonify(recipes=recipes_in_favorites)