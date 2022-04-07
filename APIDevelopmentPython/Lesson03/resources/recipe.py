from flask import request
from flask_restful import Resource
from http import HTTPStatus

from models.recipe import Recipe, recipe_list


class RecipeListResource(Resource):

    # method to get the data of only published recipe
    def get(self):

        data = []

        for recipe in recipe_list:
            if recipe.is_publish is True:
                data.append(reciped.data)

        return {'data':data}, HTTPStatus.OK

    # method to insert the data into the recipe_list
    def post(self):

        data = request.get_json()

        recipe = Recipe(name=data['name'],
                        description=data['description'],
                        num_of_servings=data['num_of_servings'],
                        cook_time=data['cook_time'],
                        directions=data['directions'])

        recipe_list.append(recipe)
        return recipe.data, HTTPStatus.CREATED


class RecipeResource(Resource):

    # Get Method of REST API with respect to recipe_id
    def get(self, recipe_id):
        recipe = next((recipe for recipe in recipe_list if recipe.id == recipe_id and recipe.is_publish == True), None)

        if recipe is None:
            return {'message':'recipe is not found'}, HTTPStatus.NOT_FOUND

        return recipe.data, HTTPStatus.OK

    # update method of Rest API with respect to recipe_id
    def put(self, recipe_id):

        data = request.json()

        recipe = next((recipe for recipe in recipe_list if recipe.id == recipe_id), None)

        if recipe is None:
            return {'message': 'recipe is not found'}, HTTPStatus.NOT_FOUND

        recipe.name = data['name']
        recipe.description = data['description']
        recipe.num_of_servings = data['num_of_servings']
        recipe.cook_time = data['cook_time']
        recipe.directions = data['directions']

        return recipe.data, HTTPStatus.OK


    # delete method of the REST API with respect to recipe id
    def delete(self, recipe_id):
        recipe = next((recipe for recipe in recipe_list if recipe.id == recipe_id), None)

        if recipe is None:
            return {'message': 'recipe is not found'}, HTTPStatus.NOT_FOUND

        recipe_list.remove(recipe)

        return {}, HTTPStatus.NO_CONTENT

class RecipePublishResource(Resource):

    # update method to update is_publish attribute
    def put(self, recipe_id):
        recipe = next((recipe for recipe in recipe_list if recipe.id == recipe_id),None)

        if recipe is None:
            return {'message':'recipe is not found'}, HTTPStatus.NOT_FOUND

        recipe.is_publish = True
        return {}, HTTPStatus.NO_CONTENT

    # delete method to set the is_publish to false
    def delete(self, recipe_id):

        recipe = next((recipe for recipe in recipe_list if recipe.id == recipe_id), None)

        if recipe is None:
            return {'message':'recipe not found'}, HTTPStatus.NOT_FOUND

        recipe.is_publish = False

        return {}, HTTPStatus.NO_CONTENT