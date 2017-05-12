import csv
import sys
import sqlite3

db = sqlite3.connect('data.db')
c = db.cursor()


def read_csv(filename, define):
    if not filename.endswith('.csv'):
        filename += '.csv'
    reader = csv.reader(open(filename))

    list_reader = list(reader)

    if define == 'f':
        column_names = [name for name in list_reader[0]]
        column_data_types = [find_types(column_data) for column_data in list_reader[1]]

        info = [(name, data_type) for name, data_type in zip(column_names, column_data_types)]

        modify = []
        for row in list_reader[1:]:
            modify.append([convert_types(ele, typping) for ele, typping in zip(row, column_data_types)])

        return info, modify
    else:
        print('Identify each column as:\nText: t\nInteger: i\nBlob: b\nReal: r\n')
        info = [(x, convert_input_data(input(x + ' is of type: '))) for x in list_reader[0]]


        modify = []
        for row in list_reader[1:]:
            modify.append([convert_types(ele, typping[1]) for ele, typping in zip(row, info)])

        return info, modify


def find_types(x):
    try:
        int(x)
        return 'INTEGER'
    except ValueError as v:
        pass
    try:
        float(x)
        return 'REAL'
    except ValueError as v:
        pass
    if x.startswith('$'):
        return 'REAL'
    else:
        try:
            str(x)
            return 'TEXT'
        except ValueError as v:
            return 'BLOB'


def convert_types(x, y):
    if y == 'INTEGER':
        return int(x)
    if y == 'REAL':
        if x.startswith('$'):
            x = x.replace('$', '')
            x = x.replace(',', '')
        return float(x)
    if y == 'TEXT':
        return str(x)
    if y == 'BLOB':
        return str(x)


def convert_input_data(input_data):
    return {'t': 'TEXT',
            'i': 'INTEGER',
            'b': 'BLOB',
            'r': 'REAL'}.get(input_data, input_data)


def create_table(header, table_name):
    c.execute('SELECT name FROM sqlite_master WHERE type = "table" AND name="'+table_name+'"')
    if c.fetchone() is not None:
        print('This table already exists.')
        sys.exit(1)

    creation = 'CREATE TABLE IF NOT EXISTS '+ table_name + '('
    for var_name, var_type in header:
        creation += var_name + ' ' + var_type + ', '
    creation = creation[0:-2] + ')'
    c.execute(creation)


def add_data(header, data, tablename):
    creation = 'INSERT INTO ' + tablename + ' VALUES(' + ('?, ' * len(header))
    creation = creation[0:-2] + ')'

    c.executemany(creation, data)
    db.commit()


if __name__ == '__main__':
    if len(sys.argv) <= 3:
        print('python csv_to_sql.py [filename] [table_name] [self-define]')
        print('[filename] = .csv file')
        print('[table_name] = name of table')
        print('[self-define] = t/f If f program will attempt to identify Column data types')
        sys.exit(1)

    _, filename, table_name, define = sys.argv

    header, data = read_csv(filename, define)
    create_table(header, table_name)
    add_data(header, data, table_name)