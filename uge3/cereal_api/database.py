import flask
import locale
from genericpath import exists
from flask_mongoengine import MongoEngine
import csv


class Cereal(MongoEngine().Document):
    name = MongoEngine().StringField()
    mfr = MongoEngine().StringField()
    type = MongoEngine().StringField()
    calories = MongoEngine().IntField()
    protein = MongoEngine().IntField()
    fat = MongoEngine().IntField()
    sodium = MongoEngine().IntField()
    fiber = MongoEngine().FloatField()
    carbo = MongoEngine().FloatField()
    sugars = MongoEngine().IntField()
    potass = MongoEngine().IntField()
    vitamins = MongoEngine().IntField()
    shelf = MongoEngine().IntField()
    weight = MongoEngine().FloatField()
    cups = MongoEngine().FloatField()
    rating = MongoEngine().FloatField()


class Database():
    def __init__(self, app: flask.Flask):
        self.db = MongoEngine()
        self.db.init_app(app)


    def _field_from_typename(self, typename):
        if 'String' == typename:
            return self.db.StringField()
        elif 'Categorical' == typename:
            return self.db.StringField()
        elif 'Int' == typename:
            return self.db.IntField()
        elif 'Float' == typename:
            return self.db.FloatField()


    def _parse_csv(self, filename):
        with open(filename, newline='\n') as csvfile:
            reader = csv.reader(csvfile, delimiter=';')
            for row in reader:
                yield row


    def import_csv(self):
        if not exists("Cereal.csv"):
            print("Error: 'Cereal.csv' not found")
            return

        # Set up locale
        locale.setlocale(locale.LC_NUMERIC, 'da_DK.UTF-8')

        # Read the headers and datatypes of the csv entries
        rows = self._parse_csv("Cereal.csv")
        headers = next(rows)
        datatypes = next(rows)

        # Set up the names and datatypes in the database
        model = Cereal()
        for name, type in zip(headers, datatypes):
            setattr(model, name, self._field_from_typename(type))

        # Insert the csv data into to database
        for row in rows:
            #model = Cereal()
            for header, dtype, data in zip(headers, datatypes, row):
                if dtype == 'Float':
                    setattr(model, header, locale.atof(data))
                else:
                    setattr(model, header, data)
            model.save()

        # Save the data in the db

