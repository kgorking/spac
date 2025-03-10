
import import_csv
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    rows = import_csv.read("Cereal.csv")
    names = next(rows)

    return names



app.run(host='0.0.0.0', port=81)