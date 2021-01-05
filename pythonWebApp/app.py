import datetime
from flask import Flask, render_template, request
from pymongo import MongoClient
import secrets


app = Flask(__name__)
client = MongoClient(secrets.MONGO_CON_STR)
app.db = client.microblog


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        entry = request.form.get('content')
        date = datetime.datetime.today().strftime('%Y-%m-%d').strip('%b %d')
        app.db.entries.insert_one({'content': entry, 'date': date})
    entries = list(app.db.entries.find({})).__reversed__()
    return render_template('index.html', entries=entries)


if __name__ == '__main__':
    app.run()
