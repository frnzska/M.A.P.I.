from db import db


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)


    @classmethod
    def find_by_id(cls, _id: int) -> "UserModel":
        users = cls.query.filter_by(id=_id)
        return users.first()

    @classmethod
    def find_by_email(cls, email: str) -> "UserModel":
        users = cls.query.filter_by(email=email)
        return users.first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
