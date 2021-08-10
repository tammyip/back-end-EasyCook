from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
load_dotenv()

def create_app(test_config=None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # to keep order of sorted dictionary passed to jsonify() function
    app.config['JSON_SORT_KEYS'] = False 

    if test_config is None: 
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_DATABASE_URI")
    else:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_TEST_DATABASE_URI")

    # Import models here for Alembic setup
    # from app.models.ExampleModel import ExampleModel
    from app.models.user import User
    from app.models.recipe import Recipe
    from app.models.plan import Plan

    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints here
    # from .routes import example_bp
    # app.register_blueprint(example_bp)
    from .routes import user_bp    
    app.register_blueprint(user_bp)
    
    from .routes import recipe_bp
    app.register_blueprint(recipe_bp)

    from .routes import plan_bp
    app.register_blueprint(plan_bp)

    CORS(app)
    return app