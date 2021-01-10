from flask_restful import Resource
from flask import request
from models.user import UserModel
from schemas.user import UserSchema
from marshmallow import EXCLUDE

ALREADY_EXISTS = "'{}' already exsits."
CREATED = 'Successfully created.'
NOT_FOUND = "'{}' not found."
DELETED = "Successfully deleted"

user_schema = UserSchema(unknown=EXCLUDE)


class UserRegister(Resource):
    def post(self):

        data = user_schema.load(request.get_json())

        if UserModel.find_by_email(data["email"]):
            return {"message": ALREADY_EXISTS.format('user')}, 400

        user = UserModel(**data)
        user.save_to_db()

        return {"message": CREATED}, 201


class User(Resource):

    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": NOT_FOUND.format('User')}, 404
        return user_schema.dump(user), 200

    @classmethod
    def delete(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": NOT_FOUND.format('User')}, 404
        user.delete_from_db()
        return {"message": DELETED}, 200