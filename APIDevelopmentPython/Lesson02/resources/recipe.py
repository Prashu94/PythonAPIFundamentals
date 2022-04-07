from flask import request
from flask_restful import Resource
from http import HTTPStatus

from models.recipe import Recipe, recipe_list

"""RecipeListResource class extends the
Resource Class from the flask_restful package,
to avoid defining GET/POST/PUT annotations"""


class RecipeListResource(Resource):
    # Method to get the list of Recipes
    def get(self):

        data = []

        for recipe in recipe_list:
            if recipe.is_publish is True:
                # .data calls the property annotation to get the data in json format
                data.append(recipe.data)

        return {'data': data}, HTTPStatus.OK

    # Method to create the recipe and add it to a list
    def post(self):

        data = request.get_json()

        recipe = Recipe(
            name=data['name'],
            description=data['description'],
            num_of_servings=data['num_of_servings'],
            cook_time=data['cook_time'],
            directions=data['directions']
        )

        recipe_list.append(recipe)

        return recipe.data, HTTPStatus.CREATED


"""RecipeResource Class Representation for operation on a single recipe 
which extends the Resource class 
for avoiding the annotations for GET/POST/PUT"""
class RecipeResource(Resource):

    # Method to get the single recipe
    def get(self, recipe_id):
        recipe = next((recipe for recipe in recipe_list if recipe.id == recipe_id and recipe.is_publish == True),None)

        if recipe is None:
            return {'message':'recipe not found'}, HTTPStatus.NOT_FOUND

        return recipe.data, HTTPStatus.OK

    # Method to update the specific recipe in a list
    def put(self, recipe_id):
        data = request.get_json()

        recipe = next((recipe for recipe in recipe_list if recipe.id == recipe_id), None)

        if recipe is None:
            return {'message':'recipe not found'}, HTTPStatus.NOT_FOUND

        recipe.name = data['name']
        recipe.description = data['description']
        recipe.num_of_servings = data['num_of_servings']
        recipe.cook_time = data['cook_time']
        recipe.directions = data['directions']

        return recipe.data, HTTPStatus.OK

class RecipePublishResource(Resource):

    # Method to update the is_publish flag of the specified recipe
    def put(self, recipe_id):
        recipe = next((recipe for recipe in recipe_list if recipe.id == recipe_id), None)

        if recipe is None:
            return {'message':'recipe is not found'}, HTTPStatus.NOT_FOUND

        recipe.is_publish = True

        return {}, HTTPStatus.NO_CONTENT

    # Method to delete the specified recipe
    def delete(self, recipe_id):
        recipe = next((receipe for recipe in recipe_list if recipe.id == recipe_id), None)

        if recipe is None:
            return {'message':'recipe not found'}, HTTPStatus.NOT_FOUND

        recipe.is_publish = False
        return {}, HTTPStatus.NO_CONTENT