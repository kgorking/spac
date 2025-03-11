from genericpath import exists
from flask import g, jsonify, request
import sqlite3
import csv


class Database:
    def __init__(self):
        self.verify_table_exists()

    def get_all_cereal(self):
        with self.get_connection() as conn:
            cur = conn.execute("SELECT * from cereals")
            rows = cur.fetchall()
            return rows if rows is not None else []

    def get_cereal(self, id: int):
        with self.get_connection() as conn:
            cur = conn.execute("SELECT * from cereals where id=?", (id,))
            row = cur.fetchone()
            return row if row is not None else []

    def verify_table_exists(self):
        if exists("data/cereals.db"):
            return

        conn = self.get_connection()
        conn.execute(
            """CREATE TABLE IF NOT EXISTS cereals(
                id INTEGER PRIMARY KEY,
                name TEXT,
                mfr TEXT,
                type TEXT,
                calories INTEGER,
                protein INTEGER,
                fat INTEGER,
                sodium INTEGER,
                fiber Float,
                carbo Float,
                sugars INTEGER,
                potass INTEGER,
                vitamins INTEGER,
                shelf INTEGER,
                weight Float,
                cups Float,
                rating Float
            )"""
        )
        self._import_csv()


    def get_connection(self):
        if "db" not in g:
            g.db = sqlite3.connect("data/cereals.db")

            # Converts a row to a {key: value} dictionary
            # TODO lots of duplication of key names
            def dict_factory(cursor, row):
                fields = [column[0] for column in cursor.description]
                return {key: value for key, value in zip(fields, row)}

            g.db.row_factory = dict_factory
        return g.db

    def _import_csv(self):
        if not exists("data/Cereal.csv"):
            print("Error: 'Cereal.csv' not found")
            exit(1)

        # Read the headers and datatypes of the csv entries
        with open("data/Cereal.csv", newline="\n") as csvfile:
            rows = csv.reader(csvfile, delimiter=";")
            headers = next(rows)
            datatypes = next(rows)

            # Insert the csv data into to database
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.executemany(
                """
                INSERT INTO
                cereals (name,mfr,type,calories,protein,fat,sodium,fiber,carbo,sugars,potass,vitamins,shelf,weight,cups,rating)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                rows,
            )
            conn.commit()
