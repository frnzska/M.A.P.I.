import sqlite3


class ItemModel():

    def __init__(self, name, price):
        self.name = name
        self.price = price


    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        query = """SELECT * FROM items WHERE name=?"""
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        conn.close()
        return row


    def insert(self):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        payload = self.parser.parse_args()
        query = 'INSERT INTO items VALUES(?, ?)'
        cursor.execute(query, (self.name, self.price))
        conn.commit()
        conn.close()
        return self


    def update(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()
        query = 'UPDATE items SET price=? WHERE name=?'
        cursor.execute(query, (self.price, self.name))
        connection.commit()
        connection.close()
        return self