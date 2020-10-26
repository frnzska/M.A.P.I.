import functools
import sqlite3

class User:


    def __init__(self, id, username, password, email):
        self.id = id
        self.username = username
        self.password = password
        self.email = email


    def find_by_name(cls, name):
        user = None
        con = sqlite3.connect('data.db')
        cursor = con.cursor()
        query = 'SELECT * FROM users WHERE name=?'
        results = cursor.execute(query, (name,))
        row = results.fetchone()
        con.close()
        if row:
             user = cls(*row)
        return user


    def find_by_id(cls, id):
        user = None
        con = sqlite3.connect('data.db')
        cursor = con.cursor()
        query = 'SELECT * FROM users WHERE id=?'
        results = cursor.execute(query, (id,))
        row = results.fetchone()
        con.close()
        if row:
             user = cls(*row)
        print(user)
        return user

    def find_by_email(cls, email):
        user = None
        con = sqlite3.connect('data.db')
        cursor = con.cursor()
        query = 'SELECT * FROM users WHERE email=?'
        results = cursor.execute(query, (id,))
        row = results.fetchone()
        con.close()
        if row:
             user = cls(*row)
        return user


