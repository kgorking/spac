import json
from flask import jsonify, request
from flask_restful import Api, Resource
import sqlalchemy
from models import db, Cereal

api = Api()


class CerealAPI(Resource):
    def get(self, id: int):
        cereal = Cereal.query.get(id)
        if cereal:
            return jsonify(cereal)
        else:
            return {"message": f"Cereal with id {id} not found"}, 404


class CreateCerealAPI(Resource):
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
    def delete(self, id: int):
        cereal = Cereal.query.get(id)
        if cereal:
            db.session.delete(cereal)
            db.session.commit()
            return {"message": f"cereal {id} deleted"}, 200
        else:
            return {"message": f"invalid id {id}"}, 400


api.add_resource(ListCerealAPI, "/cereal")
api.add_resource(CerealAPI, "/cereal/<int:id>")
api.add_resource(CreateCerealAPI, "/cereal/create")
api.add_resource(DeleteCerealAPI, "/cereal/delete/<int:id>")
