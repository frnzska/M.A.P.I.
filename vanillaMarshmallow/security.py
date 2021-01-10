from werkzeug.security import safe_str_cmp
from resources.user import UserModel


def authenticate(email, password):
    user = UserModel.find_by_email(email)
    if user and safe_str_cmp(password, user.password):
        return user


def identity(payload):# id stored in JWD
    user_id = payload['identity']
    return UserModel.find_by_id(user_id)
