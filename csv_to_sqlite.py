import csv
import sys
import sqlite3
import argparse


def find_types(head_ele, column_data):
    try:
        int(column_data)
        print(head_ele + ' is INTEGER')
        return 'INTEGER'
    except ValueError:
        pass
    try:
        float(column_data)
        print(head_ele + ' is REAL')
        return 'REAL'
    except ValueError:
        pass
    if column_data.startswith('$'):
        print(head_ele + ' is REAL')
        return 'REAL'
    try:
        str(column_data)
        print(head_ele + ' is TEXT')
        return 'TEXT'
    except ValueError:
        print(head_ele + ' is BLOB')
        return 'BLOB'


def convert_types(element, typing):
    try:
        if typing == 'INTEGER':
            return int(element)
        if typing == 'REAL':
            if element.startswith('$'):
                element = element.replace('$', '')
                element = element.replace(',', '')
            return float(element)
        if typing == 'TEXT':
            return str(element)
        if typing == 'BLOB':
            return str(element)
    except ValueError:
        print('"' + element + '" is not of type ' + typing + '.')
        print('Exiting...')
        sys.exit(1)


def convert_input_data(input_data):
    return {'t': 'TEXT',
            'i': 'INTEGER',
            'b': 'BLOB',
            'r': 'REAL'}.get(input_data, 'BLOB')


def create_table(header, table_name):
    creation = 'CREATE TABLE IF NOT EXISTS ' + table_name + '('
    for var_name, var_type in header:
        creation += var_name + ' ' + var_type + ', '
    creation = creation[0:-2] + ')'
    c.execute(creation)


def add_data(data, tablename):
    creation = 'INSERT INTO ' + tablename + ' VALUES(' + ('?, ' * len(data))
    creation = creation[0:-2] + ')'
    c.execute(creation, data)
    db.commit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert CSV file to SQLITE table')
    parser.add_argument('-i', action='store_true', dest='define', default=False,
                help='Set flag to identify Column types otherwise program will attempt to determine automatically.')
    parser.add_argument('filename', action='store', help='Set .csv file to read from.')
    parser.add_argument('-t', action='store', default='data', dest='table_name',
                help='Set table name. Default is data.')
    parser.add_argument('-d', action='store', default='data.db', dest='database',
                help='Set existing database to add table to. Default creates new database named data.db')

    results = parser.parse_args()
    filename = results.filename
    define = results.define
    table_name = results.table_name or 'data'
    database = results.database or 'data.db'

    if not filename.endswith('.csv'):
        filename += '.csv'
    if not database.endswith('.db'):
        database += '.db'
    print('Adding data to database "' + database + '", table "' + table_name + '", from file "' + filename + '"')

    db = sqlite3.connect(database)
    c = db.cursor()

    c.execute('SELECT name FROM sqlite_master WHERE type = "table" AND name="'+table_name+'"')
    if c.fetchone() is not None:
        print('Table "' + table_name + '" already exists.')
        print('Exiting without adding entries')
        sys.exit(1)

    reader = csv.reader(open(filename))
    row0 = next(reader)

    if define:
        print('Identify each column as:\nText: t\nInteger: i\nBlob: b\nReal: r\n')
        header_info = [(head_ele, convert_input_data(input(head_ele + ' is of type: '))) for head_ele in row0]
        create_table(header_info, table_name)
    else:
        print('Identifying variable types')
        row1 = next(reader)
        header_info = [(head_ele, find_types(head_ele, column_data)) for head_ele, column_data in zip(row0, row1)]
        create_table(header_info, table_name)
        add_data([convert_types(element, typing[1]) for element, typing in zip(row1, header_info)], table_name)

    for row in reader:
        add_data([convert_types(element, typing[1]) for element, typing in zip(row, header_info)], table_name)
    print('Data successfully added')
