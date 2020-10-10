import mysql.connector

dir_name = '/media/storage/bloomberg'

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='etf',
    auth_plugin='mysql_native_password',
)

create_sql = 'CREATE TABLE IF NOT EXISTS bloomberg (' + \
    'id INT(11) AUTO_INCREMENT,' + \
    'name VARCHAR(32) NOT NULL, ' + \
    'return_3_months FLOAT,' + \
    'return_ytd FLOAT,' + \
    'return_1_year FLOAT,' + \
    'return_3_year FLOAT,' + \
    'return_5_year FLOAT,' + \
    'inception_date DATE, ' + \
    'primary key (id), ' + \
    'UNIQUE(name) );'

mycursor = mydb.cursor()
mycursor.execute(create_sql)
mydb.commit()

col_names = {
    'Name': 'name',
    '3 Month Return': 'return_3_months',
    'YTD Return': 'return_ytd',
    '1 Year Return': 'return_1_year',
    '3 Year Return': 'return_3_year',
    '5 Year Return': 'return_5_year',
    'Inception Date': 'inception_date',
}

col_names_expression = '(' + ', '.join(col_names.values()) + ')'
col_values_expression = '(' + ', '.join(['%s' for x in range(len(col_names))]) + ')'
