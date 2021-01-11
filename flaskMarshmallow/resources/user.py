from flask_restful import Resource
from flask import request
from models.user import UserModel
from schemas.user import UserSchema
from marshmallow import EXCLUDE
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt,
)
from blacklist import BLACKLIST

ALREADY_EXISTS = "'{}' already exsits."
CREATED = "Successfully created."
NOT_FOUND = "'{}' not found."
DELETED = "Successfully deleted"
INVALID_CREDENTIALS = "Invalid credentials"
USER_LOGGED_OUT = 'Successfully logged out'

user_schema = UserSchema(unknown=EXCLUDE)


class UserRegister(Resource):
    def post(self):
        user = user_schema.load(request.get_json())
        if UserModel.find_by_email(user.email):
            return {"message": ALREADY_EXISTS.format(user.email)}, 400
        user.save_to_db()
        return {"message": CREATED}, 201


class User(Resource):
    @classmethod
    @jwt_required
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": NOT_FOUND.format("User")}, 404
        return user_schema.dump(user), 200

    @classmethod
    @jwt_required
    def delete(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": NOT_FOUND.format("User")}, 404
        user.delete_from_db()
        return {"message": DELETED}, 200

class UserLogin(Resource):
    @classmethod
    def post(cls):

        data = request.get_json()
        login_user = user_schema.load(data)
        user = UserModel.find_by_email(login_user.email)

        if user and safe_str_cmp(login_user.password, user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {"access_token": access_token, "refresh_token": refresh_token}, 200

        return {"message": INVALID_CREDENTIALS}, 401

class UserLogout(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        jti = get_raw_jwt()["jti"]  # jti is "JWT ID", a unique identifier for a JWT.
        user_id = get_jwt_identity()
        BLACKLIST.add(jti)
        return {"message": USER_LOGGED_OUT.format(user_id)}, 200


class TokenRefresh(Resource):
    @classmethod
    @jwt_refresh_token_required
    def post(cls):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200