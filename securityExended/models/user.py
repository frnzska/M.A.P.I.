import functools
import sqlite3

from securityExended.db import db


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(100))
    email = db.Column(db.String(100))

    def __init__(self, email, password):
        self.password = password
        self.email = email

    @classmethod
    def find_by_id(cls, id):
        users = cls.query.filter_by(id=id)
        return users.first()

    @classmethod
    def find_by_email(cls, email):
        users = cls.query.filter_by(email=email)
        return users.first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()
