from app import app
from db import db

db.init_app(app)


@app.before_first_request
def create_tables():
    # inital table setup
    db.create_all()
