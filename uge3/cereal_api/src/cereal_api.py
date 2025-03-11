from genericpath import exists
from flask import Flask, g, request
import sqlite3
from database import Database

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
    return "/cereal"


@app.route("/cereal/<int:id>")
def get_cereal_by_id(id: int):
    return db.get_cereal(id)


@app.route("/cereal")
def get_cereals():
    return db.get_all_cereal()


@app.route("/create", methods=["POST"])
def create():
    pass


@app.route("/delete", methods=["DELETE"])
def delete():
    pass


@app.route("/update", methods=["PUT"])
def update():
    pass


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=81)
