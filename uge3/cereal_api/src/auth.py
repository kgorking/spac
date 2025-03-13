from flask import request
from flask_login import login_user, logout_user, login_required, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash

from cereal_api import app
from user import User

login_manager = LoginManager()
#login_manager.init_app(app)
#login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/login", methods=["POST"])
def login():
    if request.method != "POST":
        return {"message", "bad request"}, 402

    email = request.form["email"]
    password = request.form["password"]
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        login_user(user)
        return "ok"
    else:
        return "Login failed. Check your email and password."


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return "You have been logged out."
