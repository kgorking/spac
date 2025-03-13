import csv
from os.path import exists
from models import db, Cereal

def import_csv(filename):
    if not exists(filename):
        print(f"Error: '{filename}' not found")
        return

    # Read the headers and datatypes of the csv entries
    with open(filename, newline="\n") as csvfile:
        rows = csv.reader(csvfile, delimiter=";")
        headers = next(rows)
        datatypes = next(rows)

        for row in rows:
            new_cereal = Cereal()
            for k, v in zip(headers, row):
                if k == 'rating':
                    v = v.replace('.', '')  # Remove thousand separators
                    v = '0.' + v            # Convert to [0-1] value
                setattr(new_cereal, k, v)
            db.session.add(new_cereal)
        db.session.commit()
