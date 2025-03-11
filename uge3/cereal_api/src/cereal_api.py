from genericpath import exists
from flask import Flask, request, jsonify, g
import sqlite3
from database import Database

# Set up the app
app = Flask(__name__)


@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()


@app.route("/")
def index():
    with db.get_connection() as conn:
        conn.row_factory = sqlite3.Row
        if "id" in request.args:
            cur = conn.execute(
                "SELECT * from cereals where id=?", (request.args["id"],)
            )
        else:
            cur = conn.execute("SELECT * from cereals")
        rows = cur.fetchall()
        return jsonify([dict(row) for row in rows])


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
    # Set up the database
    with app.app_context():
        db = Database()

    app.run(debug=True, host="0.0.0.0", port=81)
