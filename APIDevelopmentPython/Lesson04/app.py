from flask import Flask
from flask_migrate import Migrate
from flask_restful import Api

from config import Config
from extensions import db
from models.user import User
from resources.recipe import RecipeListResource, RecipeResource, RecipePublishResource
from resources.user import UserListResource


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    register_extensions(app)
    register_resources(app)

    return app


def register_extensions(app):
    # Initialize the Flask App in the database
    db.init_app(app)
    # transfer the object to the database.
    migrate = Migrate(app, db)


def register_resources(app):
    # Method to register the API
    api = Api(app)

    api.add_resource(UserListResource, '/users')
    api.add_resource(RecipeListResource, '/recipes')
    api.add_resource(RecipeResource, '/recipes/<int:recipe_id>')
    api.add_resource(RecipePublishResource, '/recipes/<int:recipe_id>/publish')
