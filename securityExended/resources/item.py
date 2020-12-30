from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, fresh_jwt_required
from securityExended.models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', default=0.0)

    @jwt_required
    def get(self, name):
        item = ItemModel.find_by_name(name)
        return item.json() if item else None, 200 if item else 404 # return valid json representation


    @fresh_jwt_required
    def post(self, name):
        #eg.  server/item/fancy_hat -> post(name=fancy_hat)
        #price = request.get_json() # get request body, payload
        item = ItemModel.find_by_name(name)
        if item:
            return {'message': f'Item with name {name} already exists.'}, 400
        payload = self.parser.parse_args()
        item = ItemModel(name, payload['price'])
        item.save_to_db()
        return item.json(), 201


    @fresh_jwt_required
    def put(self, name):
        payload = self.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if not item:
            item = ItemModel(name=name, price=payload['price'])
            return {'message': f'Item with name {name} created.'}, 200
        item.price = payload['price']
        item.save_to_db()
        return item.json(), 201

    @fresh_jwt_required
    def delete(self, name):
        item = ItemModel.find_by_name(name=name)
        if item:
            item.delete_from_db()
        return {'message': f'Item with name {name} deleted'}


class ItemList(Resource):

    @jwt_required
    def get(self):
        items = ItemModel.query.all()
        return {'items': [item.json() for item in items]}

