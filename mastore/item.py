from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
import sqlite3

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('some_payload_field')

    @classmethod
    def find_by_name(cls, name):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        query = """SELECT * FROM items WHERE name=?"""
        result = cursor.execute(query, (name,))
        row = result.fetchone()
        conn.close()
        return row


    @classmethod
    def insert(cls, item):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        payload = cls.parser.parse_args()
        query = 'INSERT INTO items VALUES(?, ?)'
        cursor.execute(query, (item['name'], item['some_payload_field']))
        conn.commit()
        conn.close()
        return item


    @jwt_required() # first login, via auth endpoint, in header Authorisation: JWT keykeykey..
    def get(self, name):
        item = self.find_by_name(name)
        return {'item': item}, 200 if item else 404 # return valid json representation


    #@jwt_required()
    def post(self, name):
        #eg.  server/item/fancy_hat -> post(name=fancy_hat)
        #some_payload_field = request.get_json() # get request body, payload
        item = self.find_by_name(name)
        if item:
            return {'message': f'Item with name {name} already exists.'}, 400
        payload = self.parser.parse_args()
        item = {'name': name, 'some_payload_field': payload['some_payload_field']}
        self.insert(item)
        response = {'item': item}
        return response, 201


    #@jwt_required()
    def put(self, name):
        payload = self.parser.parse_args()
        new_item = {'name': name, 'some_payload_field': payload['some_payload_field']}
        item = self.find_by_name(name)
        if not item:
            self.insert(new_item)
            return {'message': f'Item with name {name} created.'}, 200

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'UPDATE items SET price=? WHERE name=?'
        cursor.execute(query, (new_item['some_payload_field'], name))

        connection.commit()
        connection.close()
        return new_item, 201


    def delete(self, name):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        query = 'DELETE FROM items WHERE name=?'
        cursor.execute(query, (name,))
        conn.commit()
        conn.close()
        return {'message': 'Item deleted'}


class ItemList(Resource):

    def get(self):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        query = 'SELECT * FROM items'
        result = cursor.execute(query)
        items = [{'name': row[0], 'some_payload_field': row[1]} for row in result]
        conn.close()
        return {'items': items}

