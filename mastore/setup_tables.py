import sqlite3

connection = sqlite3.connect('data.db')

cursor = connection.cursor()

# MUST BE INTEGER
# This is the only place where int vs INTEGER matters—in auto-incrementing columns
create_table = 'CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, email text, password text)'
cursor.execute(create_table)
test_user=(1,'yo@mo.so','1234')
cursor.execute(f"INSERT INTO users VALUES {test_user}")


create_table = 'CREATE TABLE IF NOT EXISTS items (id INTEGER PRIMARY KEY, name text, price real)'
cursor.execute(create_table)

connection.commit()

connection.close()
