from werkzeug.security import safe_str_cmp
from models import db, User


def authenticate(username, password):
    user = User.query.get(name=username)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user

def identity(payload):
    user_id = payload['identity']
    return User.query.get(id=user_id)

