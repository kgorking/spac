import locale
from genericpath import exists
from flask import g
import sqlite3
import csv


class Database():
    def __init__(self):
        self.verify_table_exists()


    def verify_table_exists(self):
        conn = self.get_connection()
        cur = conn.execute('SELECT name FROM sqlite_master WHERE type="table" AND name="cereals";')
        if not cur.fetchone():
            conn.execute("""CREATE TABLE IF NOT EXISTS
            cereals(
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
            )""")


    def get_connection(self):
        if 'db' not in g:
            g.db = sqlite3.connect('cereal.db')
        return g.db


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


        # Insert the csv data into to database
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.executemany("insert into cereals values (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", rows)

        # test
        cursor.execute('SELECT * FROM cereals')
        rows = cursor.fetchall()
        for row in rows:
            print(row)