from marshmallow import Schema, fields

class UserSchema(Schema):

    class Meta:
        load_only = ('password',) # no returning/dumping of password, just receiving. Note its tuple
        dump_only = ('user_id',)
