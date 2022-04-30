from flask import request
from flask_restful import Resource
from http import HTTPStatus

from models.recipe import Recipe, recipe_list


# Class Representation for adding Recipe data to recipe_list, get the data from the recipe_list
# Extends the Resource class from flask_restful to avoid adding @app.route method to each method.
class RecipeListResource(Resource):

    # method to get the data of only published resources
    def get(self):

        data = []

        for recipe in recipe_list:
            if recipe.is_published is True:
                data.append(recipe.data)

        return {'data': data}, HTTPStatus.OK

    # method to post the data to the database
    def post(self):

        data = request.get_json()

        recipe = Recipe(name=data['name'],
                        description=data['description'],
                        num_of_servings=data['num_of_servings'],
                        cook_time=data['cook_time'],
                        directions=data['directions'])

        recipe_list.append(recipe)
        return recipe.data, HTTPStatus.OK


# Class Representation to get, put, delete individual record from the database
# Extends the Resource class to avoid the @app.routes annotation
class RecipeResource(Resource):

    # Get Method to get the specific recipe_id
    def get(self, recipe_id):
        # Loop through the recipe_list
        recipe = next((recipe for recipe in recipe_list if recipe.id == recipe_id and recipe.is_publish == True), None)

        # check if None
        if recipe is None:
            return {'message': 'recipe is not found'}, HTTPStatus.NOT_FOUND

        return recipe.data, HTTPStatus.OK

    # Update method to update the specific recipe_id in the list
    def put(self, recipe_id):

        # Get the data to be updated
        data = request.get_json()

        # Get The existing recipe from the database
        recipe = next((recipe for recipe in recipe_list if recipe.id == recipe_id), None)

        if recipe is None:
            return {'message': 'recipe is not found'}, HTTPStatus.NOT_FOUND

        # Else update the required parameters of the recipe object
        recipe.name = data['name']
        recipe.description = data['description']
        recipe.num_of_servings = data['num_of_servings']
        recipe.cook_time = data['cook_time']
        recipe.directions = data['directions']

        return recipe.data, HTTPStatus.OK

    # Delete method to delete the specific id from the list
    def delete(self, recipe_id):

        recipe = next((recipe for recipe in recipe_list if recipe.id == recipe_id), None)

        if recipe is None:
            return {'message': 'recipe is not found'}, HTTPStatus.NOT_FOUND

        recipe_list.remove(recipe)

        return {}, HTTPStatus.NO_CONTENT


# Class Representation for Publishing the resource to the database
# Extends the Resource class to avoid @app.route method on each annotation
class RecipePublishResource(Resource):

    # Update the is_publish flag in the recipe object for the specific resource
    def put(self, recipe_id):
        # Get the specific recipe from the list
        recipe = next((recipe for recipe in recipe_list if recipe.id == recipe_id), None)

        if recipe is None:
            return {'message': 'recipe is not found'}, HTTPStatus.NOT_FOUND

        recipe.is_publish = True
        return {}, HTTPStatus.NO_CONTENT

    # Delete method to set the is_publish to false
    def delete(self, recipe_id):
        # Get the specific recipe from the list
        recipe = next((recipe for recipe in recipe_list if recipe.id == recipe_id), None)

        if recipe is None:
            return {'message':'recipe is not found'}, HTTPStatus.NOT_FOUND

        recipe.is_publish = False
        return {}, HTTPStatus.NO_CONTENT




