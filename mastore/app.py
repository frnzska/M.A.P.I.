import os
import datetime
from flask import Flask
from flask_restful import Api  # enforce REST principles
from flask_jwt import JWT

from mastore.security import authenticate, identity
from mastore.resources.item import Item, ItemList
from mastore.resources.user import UserRegister


app = Flask(__name__)
app.secret_key = "test"  # for jwt exchange token

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///data.db"
)
app.config[
    "SQLALCHEMY_TRACK_MODIFICATIONS"
] = False  # turns of flask sqlchemy modificatinon tracker, sql aclchemy tracker is there
app.config["PROPAGATE_EXCEPTIONS"] = True

app.config["JWT_EXPIRATION_DELTA"] = datetime.timedelta(
    days=365
)  # change config before creating JWT instance
app.config["JWT_AUTH_URL_RULE"] = "/login"  # default is '/auth'
app.config[
    "JWT_AUTH_USERNAME_KEY"
] = "email"  # authentication with email instead of username (default)

jwt = JWT(
    app, authenticate, identity
)  # creates endpoint  and checks via authenticate and identity method,
# here email and password need to be in request body and match those on server.
# returns access_token which needs to be assinged in header if jwt_required for an endpoint, here: get
# header: 'Authorisaton': 'JWT <the access token>'. BTW its the id stored in JWT token


# @app.before_first_request # in run.py
# def create_tables():
#    db.create_all()

api = Api(app)
api.add_resource(Item, "/item/<name>")  # name as param in methods at this endpoint
api.add_resource(ItemList, "/itemlist")
api.add_resource(UserRegister, "/register")

if __name__ == "__main__":
    from mastore.db import db  # avoid circular import

    db.init_app(app)
    app.run(port=5000, debug=True)
