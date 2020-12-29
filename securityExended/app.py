import os
import datetime
from flask import Flask
from flask_restful import Api  # enforce REST principles
from flask_jwt_extended import JWTManager

from securityExended.resources.user import UserRegister, UserLogin
from securityExended.resources.item import Item, ItemList



app = Flask(__name__)
app.secret_key = 'test' # for jwt_extended could set to app.config['JWT_SECRET_KEY']

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # turns of flask sqlchemy modificatinon tracker, sql aclchemy tracker is there
app.config['PROPAGATE_EXCEPTIONS'] = True

app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(days=365) # change config before creating JWT instance


# implementation of authenticate and identity function in user resource and create auth or login endpoint ourselves
jwt = JWTManager(app)

api = Api(app)
api.add_resource(UserRegister, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(Item, '/item/<name>') # name as param in methods at this endpoint
api.add_resource(ItemList, '/itemlist')

if __name__ == '__main__':
    from mastore.db import db # avoid circular import
    db.init_app(app)
    app.run(port=5000, debug=True)
