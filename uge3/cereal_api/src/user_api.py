from flask import request
from flask_restful import Resource
from werkzeug.security import generate_password_hash
from user import User
from cereal_api import db
from app import api


class UserAPI(Resource):
    def get(self, user_id):
        user = User.query.get(user_id)
        if user:
            return {'id': user.id, 'username': user.username, 'email': user.email}, 200
        return {'message': 'User not found'}, 404

    def delete(self, user_id):
        """Delete a user by ID."""
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return {'message': 'User deleted'}, 200
        return {'message': 'User not found'}, 404


class AddUserAPI(Resource):
    def post(self):
        """Add a new user."""
        data = request.get_json()
        if not data or not all(key in data for key in ('username', 'email', 'password')):
            return {'message': 'Invalid input'}, 400

        hashed_password = generate_password_hash(data['password'], method='sha256')
        new_user = User(username=data['username'], email=data['email'], password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return {'message': 'User added successfully', 'id': new_user.id}, 201


api.add_resource(UserAPI, '/users/<int:user_id>')
api.add_resource(AddUserAPI, '/users')
