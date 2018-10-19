from flask import Flask, request, jsonify
import json_key_values
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import *


app = Flask(__name__)

POSTGRES = {
    'user': 'postgres',
    'pw': '1234',
    'db': 'postgres',
    'host': 'localhost',
    'port': '5432',
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = create_engine('postgresql://%(user)s:\%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES)

@app.route('/api/user/add', methods=['POST'])
def add_user():
    content = dict(request.get_json())
    username = content.get(json_key_values.username)
    password = content.get(json_key_values.password)
    level = content.get(json_key_values.level)
    metadata = MetaData()

    db.execute('CREATE TABLE IF NOT EXISTS films2 (title text, director text, year text)')
    return 'ok'


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/api/json_example', methods=['POST'])
def example():
    content = request.json
    return jsonify(content)


if __name__ == '__main__':
    app.run()