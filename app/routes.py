from flask import Blueprint, request, jsonify, make_response
from app import db
from app.models.user import User
from app.models.recipe import Recipe
from app.models.plan import Plan

user_bp = Blueprint("user", __name__, url_prefix="/user")
recipe_bp = Blueprint("recipes", __name__, url_prefix="/favorites")
plan_bp = Blueprint("plans", __name__, url_prefix="/plans")

# USERS
################################################################
# Create an user
@user_bp.route("", methods=["POST"], strict_slashes=False)
def create_user():
    request_body = request.get_json()
    if ("name" not in request_body 
        or "email" not in request_body): 
        return jsonify(details = f'Invalid data'), 400

    new_user = User(name=request_body["name"],
                    email=request_body["email"])  
    db.session.add(new_user)
    db.session.commit()
    print(new_user)
    return jsonify(user_id=new_user.user_id, name=new_user.name, email=new_user.email), 201

# Add a recipe to Favorites
@user_bp.route("/<user_id>>/favorites", methods=["POST"], strict_slashes=False)
def add_recipe_to_user(user_id):
    request_body = request.get_json()
    if ("title" not in request_body
    or "image" not in request_body
    or "url" not in request_body):  
        return jsonify(details = f'Invalid data'), 400
    new_recipe_in_user = Recipe(title=request_body["title"],
                                image=request_body["image"],
                                url=request_body["url"],
                                user_id=user_id)
    db.session.add(new_recipe_in_user)
    db.session.commit()
    return jsonify(new_recipe_in_user.to_json()), 200

# Delete a recipe in Favorites
@user_bp.route("/<user_id>/<recipe_id>", methods=["DELETE"], strict_slashes=False)
def delete_card(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    db.session.delete(recipe)
    db.session.commit()
    return jsonify(recipe = f'Recipe {recipe.recipe_id} "{recipe.title}" successfully deleted')

### List all recipes saved in Favorites by an user ###
@user_bp.route("/<user_id>/favorites", methods=["GET"], strict_slashes=False)
def view_recipes_in_favorites(user_id):

    user = User.query.get_or_404(user_id)

    recipes = user.recipes # [{}, {}, {}]
    recipes_in_favorites = [recipe.to_json() for recipe in recipes if recipes]
    return jsonify(recipes=recipes_in_favorites)