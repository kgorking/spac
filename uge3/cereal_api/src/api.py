import json
from flask import jsonify, request
from flask_restful import Api, Resource
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
import sqlalchemy
from models import db, Cereal, User


class CerealAPI(Resource):
    def get(self, id: int):
        cereal = Cereal.query.get(id)
        if cereal:
            return jsonify(cereal)
        else:
            return {"message": f"Cereal with id {id} not found"}, 404

    @login_required
    def post(self):
        data = json.loads(request.data)
        new_cereal = Cereal(**data)
        db.session.add(new_cereal)
        try:
            db.session.commit()
            return {"id": new_cereal.id}, 201
        except sqlalchemy.exc.IntegrityError as e:
            return {"error": str(e)}, 400


class ListCerealAPI(Resource):
    def get(self):
        if request.args:
            return jsonify(Cereal.query.filter_by(**request.args).all())
        else:
            cereals = Cereal.query.all()
            return jsonify(cereals)


class DeleteCerealAPI(Resource):
    @login_required
    def delete(self, id: int):
        cereal = Cereal.query.get(id)
        if cereal:
            db.session.delete(cereal)
            db.session.commit()
            return {"message": f"cereal {id} deleted"}, 200
        else:
            return {"message": f"invalid id {id}"}, 400


class AuthAPI(Resource):
    @login_required
    def get(self):
        logout_user()
        return "logged out", 200

    def post(self):
        email = request.form["email"]
        password = request.form["password"]
        user: User = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            if login_user(user, remember=True):
                return "ok", 200
            else:
                return "error", 401
        else:
            return "Login failed. Check your email and password.", 401


# Set up api routes
api = Api()
api.add_resource(ListCerealAPI, "/cereal")
api.add_resource(CerealAPI, "/cereal/create", "/cereal/<int:id>")
api.add_resource(DeleteCerealAPI, "/cereal/delete/<int:id>")
api.add_resource(AuthAPI, "/login", "/logout")
