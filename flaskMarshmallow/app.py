import os
import datetime
from flask import Flask, jsonify
from marshmallow import ValidationError
from flask_restful import Api  # enforce REST principles
from flask_jwt_extended import JWTManager

from resources.user import UserRegister, User, UserLogin, TokenRefresh, UserLogout
from resources.store import Store, StoreList
from resources.item import Item, ItemList
from ma import ma
from blacklist import BLACKLIST

app = Flask(__name__)
app.secret_key = "test"  # for jwt exchange token

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///data.db"
)
app.config[
    "SQLALCHEMY_TRACK_MODIFICATIONS"
] = False  # turns of flask sqlchemy modificatinon tracker, sql aclchemy tracker is there
app.config["PROPAGATE_EXCEPTIONS"] = True # since we have @app.errorhandler this needs to be true
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=7)
app.config["JWT_AUTH_URL_RULE"] = "/login"  # default is '/auth'
app.config[
    "JWT_AUTH_USERNAME_KEY"
] = "email"  # authentication with email instead of username (default)

jwt = JWTManager(app)

@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err): # less verbose in resource files, Validation Errors propagated till here, no need to catch there
    return jsonify(err.messages), 400

#Blacklist checking for logouts
app.config["JWT_BLACKLIST_ENABLED"] = True  # enable blacklist feature
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = [
    "access",
    "refresh",
]
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token["jti"] in BLACKLIST


api = Api(app)
api.add_resource(User, "/user/<int:user_id>")
api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, "/login")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")
api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")


api.add_resource(TokenRefresh, "/refresh")
api.add_resource(UserLogout, "/logout")

@app.before_first_request # in run.py
def create_tables():
   db.create_all()

if __name__ == "__main__":
    from db import db  # avoid circular import

    db.init_app(app)
    ma.init_app(app)  # link Marschmallow schema
    app.run(port=5000, debug=True)


"""
Linking UserModel directly in the Schema with flask_marshmellow -> marshmellow loads UserModel objects directly 
and not dicts income_data >> model object
"""
