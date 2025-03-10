import csv

def read(filename):
    with open(filename, newline='\n') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:
            yield row
