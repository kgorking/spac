from flask import Flask
from csv_importer import import_csv
from werkzeug.security import generate_password_hash

app = Flask(__name__)
app.instance_path = "data"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cereals.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "6d6a710e529aeaaa20dbcaf5edd1519501522b5ba5bb172132de898a2783a4cd"
app.secret_key = "6d6a710e529aeaaa20dbcaf5edd1519501522b5ba5bb172132de898a2783a4cd"

# Init Auth
from auth import login_manager
login_manager.init_app(app)

# Init API
from api import api
api.init_app(app)

# Init database
from models import db, Cereal, User
db.init_app(app)


if __name__ == "__main__":
    with app.app_context() as ctx:
        # Create database tables if needed
        db.create_all()

        # Import .csv data if db is empty
        if 0 == len(Cereal.query.all()):
            print("Importing .csv file...")
            import_csv("data/cereal.csv")

        # Add default user if needed
        user = db.session.get(User, 1)
        if not user:
            print("Creating default user 'user' with password 'password'...")
            hashed_pw = generate_password_hash('password')
            user = User(name='user', password=hashed_pw, email='user@password.com')
            db.session.add(user)
            db.session.commit()

    # Start the server
    app.run(debug=False, host="0.0.0.0", port=81)
