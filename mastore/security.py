from werkzeug.security import safe_str_cmp
from mastore.user import User

#todo
users = [User(1, 'cate', '1234')]


# helper dicts to speed up search
username_mapping ={u.username: u for u in users}
userid_mapping ={u.id: u for u in users}

def authenticate(username, password):
    user = username_mapping.get(username, None)
    if user and safe_str_cmp(password, user.password):
        return user


def identity(payload):
    user_id = payload['identity']
    return userid_mapping.get(user_id, None)

