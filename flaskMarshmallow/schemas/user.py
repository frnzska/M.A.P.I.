from models.user import UserModel
from ma import ma

class UserSchema(ma.SQLAlchemyAutoSchema): # app initialisation in app.py
    class Meta: # keyword variables!
        model = UserModel  # checks fields defined in Usermodel and creating them
        load_only = (
            "password",
        )  # no returning/dumping of password, just receiving. Note its tuple
        dump_only = ("user_id",)
        load_instance = True # without this dict instaead of usermodel obj loaded
