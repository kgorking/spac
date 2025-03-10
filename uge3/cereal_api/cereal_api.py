from flask import Flask, request, jsonify
from database import Database, Cereal

# Set up the app and database
app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
    'db': 'cereal_db',
    'host': 'localhost',
    'port': 27017
}
db = Database(app)

@app.route('/')
def index():
    db.import_csv()
    return Cereal.objects()


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


app.run(host='0.0.0.0', port=81)
