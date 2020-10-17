from flask import Flask, jsonify, render_template, request
from flask_restful import Resource, Api # enforce REST principles
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

    @jwt_required() # first login, via auth endpoint
    def get(self, name):
        item = next(filter(lambda i: i['name'] == name, items), None) # first one
        return {'item': item}, 200 if item else 404 # return valid json representation


    def post(self, name):
        #eg.  server/item/fancy_hat -> post(name=fancy_hat)
        data = request.get_json() # get request body, payload
        item = {'name': name, 'some_payload_field': data['example_field']}
        response = {'item': item}
        if next(filter(lambda i: i['name'] == name, items), None):
            return response, 400
        items.append(item)
        return response, 201


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