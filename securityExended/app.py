import os
import datetime
from flask import Flask
from flask_restful import Api  # enforce REST principles
from flask_jwt_extended import JWTManager

from securityExended.resources.user import UserRegister, UserLogin
from securityExended.resources.item import Item, ItemList

from securityExended.blacklist import BLACKLIST

app = Flask(__name__)
app.secret_key = "test"  # for jwt_extended could set to app.config['JWT_SECRET_KEY']

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///data.db"
)
app.config[
    "SQLALCHEMY_TRACK_MODIFICATIONS"
] = False  # turns of flask sqlchemy modificatinon tracker, sql aclchemy tracker is there
app.config["PROPAGATE_EXCEPTIONS"] = True

app.config["JWT_EXPIRATION_DELTA"] = datetime.timedelta(
    days=7
)  # change config before creating JWT instance

app.config["JWT_BLACKLIST_ENABLED"] = True  # enable blacklisting
app.config["JWT_BLACKLIST_TOKEN_CHECKS"] = [
    "access",
    "refresh",
]  # allow blacklisting for access and refresh tokens


# implementation of authenticate and identity function in user resource and create auth or login endpoint ourselves
jwt = JWTManager(app)

api = Api(app)
api.add_resource(UserRegister, "/register")
api.add_resource(UserLogin, "/login")
api.add_resource(Item, "/item/<name>")  # name as param in methods at this endpoint
api.add_resource(ItemList, "/itemlist")

# check if token is blacklisted, and will be called automatically when blacklist above is enabled in app.config['JWT_BLACKLIST_ENABLED'] = True
@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token["jti"] in BLACKLIST


@jwt.expired_token_loader  # called whenever jwt tokens expires
def token_expired_callback():
    return {"msg": "Token expired"}, 401


# other decorators are e.g. @jwt.needs_fresh_token_loader, @jwt.invalid_token_loader etc.

if __name__ == "__main__":
    from mastore.db import db  # avoid circular import

    db.init_app(app)
    app.run(port=5000, debug=True)
