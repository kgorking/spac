from flask import Flask, request, jsonify, g
import sqlite3
from database import Database

# Set up the app and database
app = Flask(__name__)

with app.app_context():
    db = Database()


#def get_db():
#    if 'db' not in g:
#        g.db = sqlite3.connect('cereal.db')
#    return g.db


@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    db.import_csv()
    return "tete"


@app.route('/read', methods=['GET'])
def read():
    pid = request.args.get('id')
    return pid


@app.route('/create', methods=['POST'])
def create():
    pass

@app.route('/delete', methods=['DELETE'])
def delete():
    pass

@app.route('/update', methods=['PUT'])
def update():
    pass


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=81)
