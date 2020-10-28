from werkzeug.security import safe_str_cmp
from mastore.user import User




def authenticate(email, password):
    user = User.find_by_email(email)
    if user and safe_str_cmp(password, user.password):
        return user


def identity(payload):# id stored in JWD
    user_id = payload['identity']
    return User.find_by_id(user_id)

