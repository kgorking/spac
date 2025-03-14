from genericpath import exists
import json
from flask import jsonify, make_response, request, send_file
from flask_restful import Api, Resource
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash
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
        except:
            return {"error": "exception"}, 400


class UpdateCerealAPI(Resource):
    @login_required
    def post(self):
        data = json.loads(request.data)
        num_rows_updated = Cereal.query.filter_by(id=data["id"]).update(data)
        db.session.commit()
        return {"num_rows_updated": num_rows_updated}, 200


class ListCerealAPI(Resource):
    def get(self):
        if request.args:
            # Convert to a dict I can modify
            args = request.args.to_dict()

            # Check for 'sort' argument, and remove it if found
            sort = args.get('sort', None)
            if sort:
                args.pop('sort')

            # Apply the filters
            q = Cereal.query.filter_by(**args)

            # Apply optional column sorting
            if sort:
                attr = getattr(Cereal, sort, None)
                if not attr:
                    return f"Unknown sort param '{sort}'", 400
                q = q.order_by(attr)

            return jsonify(q.all())
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


class ImageAPI(Resource):
    def get(self, id: int):
        cereal = Cereal.query.get(id)
        if cereal:
            # weird path descrepancy
            img = f'data/img/{cereal.name}.jpg'
            if exists(img):
                return send_file('../' + img, mimetype='image/jpeg')
            else:
                return "file not found", 400
        else:
            return "invalid id", 400


class LogoutAPI(Resource):
    @login_required
    def get(self):
        logout_user()
        return "logged out", 200


class LoginAPI(Resource):
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
api.add_resource(UpdateCerealAPI, "/cereal/update")
api.add_resource(CerealAPI, "/cereal/create", "/cereal/<int:id>")
api.add_resource(DeleteCerealAPI, "/cereal/delete/<int:id>")
api.add_resource(ImageAPI, "/image/<int:id>")
api.add_resource(LogoutAPI, "/logout")
api.add_resource(LoginAPI, "/login")
