from flask import request
from flask_restful import Resource
from http import HTTPStatus


from utils import hash_password
from models.user import User

"""Class Representation for Adding User extends the Resource to avoid adding @app.route to each method"""
class UserListResource(Resource):

    # method to update the user related daa
    def post(self):
        json_data = request.get_json()

        username = json_data.get('username')
        email = json_data.get('email')
        non_hash_password = json_data.get('password')

        if User.get_by_username(username):
            return {'message':'username already used'}, HTTPStatus.BAD_REQUEST

        if User.get_by_email(email):
            return {'message':'email already used'}, HTTPStatus.BAD_REQUEST

        password = hash_password(non_hash_password)
        user = User(
            username=username,
            email=email,
            password=password
        )

        # call the save method
        user.save()

        data = {
            'id':user.id,
            'username':user.username,
            'email':user.email
        }


        return data, HTTPStatus.OK