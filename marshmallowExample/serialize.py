from marshmallow import Schema, fields


class BookSchema(Schema):
    title = fields.Str()
    author = fields.Str()


class Book:
    """Basically marshmallow turns class into dictionary"""

    def __init__(self, id, title, author, description):
        self.id = id
        self.author = author
        self.title = title
        self.description = description


b = Book(123, "Deadly Martin", "The End is near", "World is going to end")
book_schema = BookSchema()

b_dict = book_schema.dump(b)
print(b_dict)
