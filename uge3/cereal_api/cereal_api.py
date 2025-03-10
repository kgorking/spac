from genericpath import exists
from flask import Flask, request, jsonify, g
import sqlite3
from database import Database

# Set up the app
app = Flask(__name__)

# Set up the database
with app.app_context():
    db = Database()


@app.teardown_appcontext
def close_db(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    with db.get_connection() as conn:
        curr = conn.execute('SELECT * from cereals')
        return jsonify(curr.fetchall())


@app.route('/read', methods=['GET'])
def read():
    pid = request.args.get('id')
    with db.get_connection() as conn:
        curr = conn.execute('SELECT * from cereals where id=?', (pid,))
        return jsonify(curr.fetchone())


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
    if not exists('cereals.db'):
        with app.app_context():
            db.import_csv()
    app.run(debug=True, host='0.0.0.0', port=81)
