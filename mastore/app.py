from flask import Flask, jsonify, render_template, request
from flask_restful import Resource, Api, reqparse # enforce REST principles
from flask_jwt import JWT, jwt_required
from mastore.security import authenticate, identity



app = Flask(__name__)
app.secret_key = 'test' # for jwt exchange token
jwt = JWT(app, authenticate, identity) # creates endpoint /auth and checks via authenticate and identity method,
# here user and password need to be in request body and match those on server.
# returns access_token which needs to be assinged in header if jwt_required for an endpoint, here: get
# header: 'Authorisaton': 'JWT <the access token>'

api = Api(app)

# todo
items = []

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('some_payload_field')

    @jwt_required() # first login, via auth endpoint
    def get(self, name):
        item = next(filter(lambda i: i['name'] == name, items), None) # first one
        return {'item': item}, 200 if item else 404 # return valid json representation


    def post(self, name):
        #eg.  server/item/fancy_hat -> post(name=fancy_hat)
        #some_payload_field = request.get_json() # get request body, payload

        if next(filter(lambda i: i['name'] == name, items), None):
            return {'message': f'Item with name {name} already exists.'}, 400

        payload = self.parser.parse_args()
        item = {'name': name, **payload}
        response = {'item': item}
        items.append(item)
        return response, 201


    def put(self, name):
        payload = self.parser.parse_args()
        item = next(filter(lambda i: i['name'] == name, items), None)
        if item:
            item.update({'name': name, **payload})
        else:
            item = {'name': name, **payload}
            items.append(item)
        return item, 201



    def delete(self, name):
        global items
        items = [x for x in items if x['name']!=name]
        return {'message': 'Item deleted'}


class ItemList(Resource):

    def get(self):
        return {'items': items}

api.add_resource(Item, '/item/<name>') # name as param in methods at this endpoint
api.add_resource(ItemList, '/itemlist')


app.run(port=5000, debug=True)