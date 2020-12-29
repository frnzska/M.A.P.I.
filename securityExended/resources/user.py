from flask_restful import Resource, reqparse
from werkzeug.security import safe_str_cmp
from securityExended.models.user import UserModel
from flask_jwt_extended import (
     create_access_token,
     create_refresh_token)

parser = reqparse.RequestParser()
parser.add_argument('email',
                    type=str,
                    required=True,
                    help="This field cannot be blank."
                    )
parser.add_argument('password',
                    type=str,
                    required=True,
                    help="This field cannot be blank."
                    )

class UserRegister(Resource):

    def post(self):
        data = parser.parse_args()
        if UserModel.find_by_email(data['email']):
            return {"message": "A user with that email already exists"}, 400
        user = UserModel(**data)
        user.save_to_db()
        return {"message": "User created successfully."}, 201


class UserLogin(Resource):
    """provides authenticate and identity function"""

    @classmethod
    def post(cls):
        data = parser.parse_args()
        user = UserModel.find_by_email(data['email'])

        if user and safe_str_cmp(user.password, data['password']):
            access_tocken = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {'access_token': access_tocken,
                    'refresh_token': refresh_token}, 200
        return {"message": "Invalid Credentials!"}, 401


