import functools
import sqlite3

class UserModel():
    __tablename__ = 'users'

    def __init__(self, id, email, password):
        self.id = id
        self.password = password
        self.email = email


    @classmethod
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
        return user

    @classmethod
    def find_by_email(cls, email):
        user = None
        con = sqlite3.connect('data.db')
        cursor = con.cursor()
        query = 'SELECT * FROM users WHERE email=?'
        results = cursor.execute(query, (email,))
        row = results.fetchone()
        con.close()
        if row:
             user = cls(*row)
        return user
