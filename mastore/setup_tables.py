import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

# MUST BE INTEGER
# This is the only place where int vs INTEGER matters—in auto-incrementing columns
create_table = 'CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text, email text)'
cursor.execute(create_table)
test_user=(1,'su','1234','yo@mo.so')
cursor.execute(f'INSERT INTO users VALUES {test_user}')
connection.commit()

create_table = 'CREATE TABLE IF NOT EXISTS items (name text PRIMARY KEY, price real)'
cursor.execute(create_table)

connection.commit()

connection.close()
