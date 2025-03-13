from dataclasses import dataclass
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

# Set up SQL Alchemy
db: SQLAlchemy = SQLAlchemy()

@dataclass
class Cereal(db.Model):
    id      : int   = db.Column(db.Integer, primary_key=True)
    name    : str   = db.Column(db.String(64), unique=True, nullable=False)
    mfr     : str   = db.Column(db.String(1), unique=False, nullable=False)
    type    : str   = db.Column(db.String(64), unique=False, nullable=False)
    calories: int   = db.Column(db.Integer)
    protein : int   = db.Column(db.Integer)
    fat     : int   = db.Column(db.Integer)
    sodium  : int   = db.Column(db.Integer)
    fiber   : float = db.Column(db.Float)
    carbo   : float = db.Column(db.Float)
    sugars  : int   = db.Column(db.Integer)
    potass  : int   = db.Column(db.Integer)
    vitamins: int   = db.Column(db.Integer)
    shelf   : int   = db.Column(db.Integer)
    weight  : float = db.Column(db.Float)
    cups    : float = db.Column(db.Float)
    rating  : float = db.Column(db.Float)


@dataclass
class User(db.Model, UserMixin):
    id       : int = db.Column(db.Integer, primary_key=True)
    name     : str = db.Column(db.String(64), unique=True, nullable=False)
    email    : str = db.Column(db.String(120), unique=True, nullable=False)
    password : str = db.Column(db.String(60), nullable=False)

    def is_authenticated(self):
        return True