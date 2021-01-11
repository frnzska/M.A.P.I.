import os
import datetime
from flask import Flask
from flask_restful import Api  # enforce REST principles
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister, User



app = Flask(__name__)
app.secret_key = 'test' # for jwt exchange token

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # turns of flask sqlchemy modificatinon tracker, sql aclchemy tracker is there
app.config['PROPAGATE_EXCEPTIONS'] = True

app.config['JWT_EXPIRATION_DELTA'] = datetime.timedelta(days=365) # change config before creating JWT instance
app.config['JWT_AUTH_URL_RULE'] = '/login' # default is '/auth'
app.config['JWT_AUTH_USERNAME_KEY'] = 'email' # authentication with email instead of username (default)

jwt = JWT(app, authenticate, identity)

api = Api(app)
api.add_resource(User, '/user/<int:user_id>')
api.add_resource(UserRegister, '/register')

#@app.before_first_request # in run.py
#def create_tables():
#    db.create_all()

if __name__ == '__main__':
    from db import db # avoid circular import
    db.init_app(app)
    app.run(port=5000, debug=True)
