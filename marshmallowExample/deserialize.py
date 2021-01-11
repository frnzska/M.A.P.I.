from marshmallow import Schema, fields, INCLUDE, EXCLUDE


class BookSchema(Schema):
    title = fields.Str()
    author = fields.Str()



incoming_payload = {'rubbish': 'rubbish',
                    'title': 'Huhu wer hat Angst vor Virginia.',
                    'stuff': 'stuffstuffstuff',
                    'author': 'Maria Martinez'}


book_schema = BookSchema(unknown=INCLUDE)
b = book_schema.load(incoming_payload)
# {'title': 'Huhu wer hat Angst vor Virginia.', 'author': 'Maria Martinez', 'stuff': 'stuffstuffstuff', 'rubbish': 'rubbish'}


book_schema = BookSchema(unknown=EXCLUDE)
b = book_schema.load(incoming_payload)
#{'title': 'Huhu wer hat Angst vor Virginia.', 'author': 'Maria Martinez'}

class Book:
    """Basically marshmallow turns class into dictionary"""

    def __init__(self, title, author):
        self.author = author
        self.title = title


book = Book(**b)