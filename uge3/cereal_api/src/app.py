from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from csv_importer import import_csv

app = Flask(__name__)
app.instance_path = 'data'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cereals.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = "Nyre-spark"
app.secret = "Nyre-spark"

# Init API
from api import api
api.init_app(app)

# Init database
from models import db, Cereal
db.init_app(app)


if __name__ == "__main__":
    # Create database tables if needed
    with app.app_context() as ctx:
        db.create_all()

        # Import .csv data if db is empty
        if 0 == len(Cereal.query.all()):
            import_csv('data/cereal.csv')

    # Start the server
    app.run(debug=True, host="0.0.0.0", port=81)
