from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource
from flask_login import LoginManager
from csv_importer import import_csv
from werkzeug.security import generate_password_hash
from flask_jwt import JWT, jwt_required, current_identity

app = Flask(__name__)
app.instance_path = "data"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cereals.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "Nyre-spark"
app.secret = "Nyre-spark"

# Init API
from api import api
api.init_app(app)

# Init database
from models import db, Cereal, User
db.init_app(app)

# Init Auth
import auth
jwt = JWT(app, auth.authenticate, auth.identity)



if __name__ == "__main__":
    with app.app_context() as ctx:
        # Create database tables if needed
        db.create_all()

        # Import .csv data if db is empty
        if 0 == len(Cereal.query.all()):
            import_csv("data/cereal.csv")

        # Add default user if needed
        user = db.session.get(User, 1)
        if not user:
            hashed_pw = generate_password_hash('password')
            user = User(name='user', password=hashed_pw, email='user@password.com')
            db.session.add(user)
            db.session.commit()
            print("Added default user 'user' with password 'password'")

    # Start the server
    app.run(debug=True, host="0.0.0.0", port=81)
