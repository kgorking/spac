from genericpath import exists
from flask import Flask, g, request
from database import Database
import sqlite3
import json

# Set up the app
app = Flask(__name__)

# Set up the database
with app.app_context():
    db = Database()


@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()


@app.route("/")
def index():
    return "Det sjove sker i '/cereal'"


@app.route("/cereal/<int:id>")
def get_cereal_by_id(id: int):
    return db.get_cereal(id)


@app.route("/cereal", methods = ['GET', 'POST', 'PUT', 'DELETE'])
def get_cereals():
    if request.method == 'GET':
        return db.get_all_cereal()
    elif request.method == 'DELETE':
        cereal = json.loads(request.data)
        return db.delete_cereal(cereal['id'])
    else:
        cereal = json.loads(request.data)
        return db.insert_or_update(cereal)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=81)
