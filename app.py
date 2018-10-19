from flask import Flask, request, jsonify
from sqlalchemy import *
import re
import json_keys

app = Flask(__name__)

POSTGRES = {
    'user': 'postgres',
    'pw': '1234',
    'db': 'postgres',
    'host': 'localhost',
    'port': '5432',
}
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = create_engine('postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES)


@app.route('/api/user/add', methods=['POST'])
def add_user():
    content = dict(request.get_json())

    username = content.get(json_keys.username)
    password = content.get(json_keys.password)
    level = content.get(json_keys.level)

    db.execute("INSERT INTO Users "
               "(login, password, accessLevel) "
               "VALUES (\'%s\', \'%s\', %s);"
               % (username, password, level))
    return 'ok'


@app.route('/api/system/db/init_tables')
def initialize_all_tables():
    content = read_file('create_tables.sql')
    return execute_sql_commands(content)


@app.route('/api/system/db/drop_tables')
def drop_all_tables():
    # todo: a good permission check is vital for this action
    content = read_file('drop_all_tables.sql')
    return execute_sql_commands(content)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/api/json_example', methods=['POST'])
def example():
    content = request.json
    return jsonify(content)


def read_file(filename):
    file = open(filename, 'r')
    content = file.read()
    file.close()
    return content


def execute_sql_commands(content):
    sql_commands = content.split(';')
    for i in sql_commands:
        # as the given string could be received from a file,
        # newline characters must be deleted
        i = re.sub('[\n]', '', i)
        if len(i) != 0:
            # we don't want to execute empty command at the end of the file
            # (as a result of a possible semicolon after the last statement)
            db.execute(i)
    return 'ok'


if __name__ == '__main__':
    app.run()
