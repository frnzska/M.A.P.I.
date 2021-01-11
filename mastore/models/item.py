from mastore.db import db


class ItemModel(db.Model):

    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    price = db.Column(db.Float(precision=2))
    store_id = db.Column(db.Integer, db.ForeignKey("stores.id"))
    store = db.relationship("StoreModel")

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __repr__(self):
        return f"{self.name}: {self.price}"

    def json(self):
        return {"name": self.name, "price": self.price}

    @classmethod
    def find_by_name(cls, name):
        results = cls.query.filter_by(
            name=name
        )  # Query form db.Model, translates to select * from __tablename__ where name=name
        return results.first()

    def save_to_db(self):
        db.session.add(self)  # session to collect objects to be eventually commited
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
