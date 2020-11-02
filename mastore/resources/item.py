from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from mastore.models.item import ItemModel
import sqlite3


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price')

    @jwt_required() # first login, via auth endpoint, in header Authorisation: JWT keykeykey..
    def get(self, name):
        item = ItemModel.find_by_name(name)
        return item.json(), 200 if item else 404 # return valid json representation


    @jwt_required()
    def post(self, name):
        #eg.  server/item/fancy_hat -> post(name=fancy_hat)
        #price = request.get_json() # get request body, payload
        item = ItemModel.find_by_name(name)
        if item:
            return {'message': f'Item with name {name} already exists.'}, 400
        payload = self.parser.parse_args()
        item = ItemModel(name, payload['price'])
        item.insert()
        return item.json(), 201


    @jwt_required()
    def put(self, name):
        payload = self.parser.parse_args()
        new_item = ItemModel(name=name, price=payload['price'])
        item = ItemModel.find_by_name(name)
        if not item:
            new_item.insert()
            return {'message': f'Item with name {name} created.'}, 200

        new_item.update()
        return new_item.json(), 201

    @jwt_required()
    def delete(self, name):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        query = 'DELETE FROM items WHERE name=?'
        cursor.execute(query, (name,))
        conn.commit()
        conn.close()
        return {'message': 'Item deleted'}


class ItemList(Resource):

    @jwt_required()
    def get(self):
        conn = sqlite3.connect('data.db')
        cursor = conn.cursor()
        query = 'SELECT * FROM items'
        result = cursor.execute(query)
        items = [{'name': row[0], 'price': row[1]} for row in result]
        conn.close()
        return {'items': items}

