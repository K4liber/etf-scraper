import glob
from utils import (
    dir_name,
    col_names,
    mydb,
    mycursor,
    col_names_expression,
    col_values_expression,
)
from bs4 import BeautifulSoup
import mysql.connector

file_names = glob.glob(dir_name + "/*.html")
records = list()


def p2f(x):
    return float(x.strip('%'))/100


def normalized_record(record):
    normed_record = dict()

    for key, value in record.items():
        try:
            normed_record[key] = p2f(value)
        except ValueError:
            if value != '--':
                if '/' in value:
                    values = value.split('/')

                    if len(values) == 3:
                        (month, day, year) = values[0], values[1], values[2]
                        normed_record[key] = '-'.join([year, month, day])
                else:
                    normed_record[key] = value
            else:
                if key == 'inception_date':
                    normed_record[key] = '1970-01-01'
                else:
                    normed_record[key] = -1.0

    return normed_record


def get_value(soup_obj, value_name: str):
    name_element = soup_obj.find("span", string=value_name)

    if name_element is None:
        return ''

    return name_element.findNext('span').findNext('span').string


def save_to_db(record):
    col_values = '(' + ', '.join(col_names.values()) + ')'
    insert_sql = 'insert into bloomberg ' + col_names_expression + ' values ' + \
                 col_values_expression
    insert_val = tuple([*(record[key] for key in col_names.values())])
    try:
        mycursor.execute(insert_sql, insert_val)
        mydb.commit()
    except mysql.connector.errors.IntegrityError:
        print("record '" + record['name'] + "' already exist.")


for file_name in file_names:
    etf_name = file_name.split('.')[0].split('/')[-1]
    file = open(file_name, 'r')
    html = file.read()
    soup = BeautifulSoup(html)
    dividend = get_value(soup, "Last Dividend Reported")

    if dividend != '--':
        continue

    record = dict()

    for val_name, col_name in col_names.items():
        record[col_name] = get_value(soup, val_name)

    normed_record = normalized_record(record)
    normed_record['name'] = etf_name
    save_to_db(normed_record)

for record in records:
    print(record)

