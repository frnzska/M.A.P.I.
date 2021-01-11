from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from mastore.models.store import StoreModel


class Store(Resource):
    def __init__(self, name):
        self.name = name

    def get(self, name):
        store = StoreModel.find_by_name(name=name)
        return store.json if store else {"message": "Store not found"}

    def post(self, name):
        store = StoreModel.find_by_name(name=name)
        if store:
            return {"message": f"Store {name} already exists"}
        else:
            store = StoreModel(name=name)
            store.save_to_db()
            return store.json()

    def delete(self, name):
        store = StoreModel.find_by_name(name=name)
        store.delete_from_db()
        return {"message": f"Store {name} deleted"}


class StoreList(Resource):
    def get(self):
        return {"stores": list(map(lambda x: x.json(), StoreModel.query.all()))}
