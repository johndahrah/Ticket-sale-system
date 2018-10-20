from flask import Flask, request, jsonify
from sqlalchemy import *
import re
import json_keys
import generate_test_db_data

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
def user_add():
    """
    sequence diagram # todo
    """
    content = dict(request.get_json())
    username, password, level = get_user_data(content)

    db.execute("INSERT INTO Users "
               "(login, password, accessLevel) "
               "VALUES (\'%s\', \'%s\', %s);"
               % (username, password, level))
    return 'ok'


@app.route('/api/user/modify', methods=['POST'])
def user_modify():
    """
    sequence diagram # todo
    # todo check if the user is in the database
    """
    content = dict(request.get_json())
    username, password, level = get_user_data(content)
    data_to_change = content.get(json_keys.change_data_type)
    if data_to_change == json_keys.level:
        db.execute('UPDATE users SET accesslevel = %s WHERE login LIKE \'%s\'' % (level, username))
        return 'ok'
    if data_to_change == json_keys.password:
        db.execute('UPDATE users SET password = %s WHERE login LIKE \'%s\'' % (password, username))
        return 'ok'
    if data_to_change == json_keys.username:
        # todo
        pass
    return 'nothing has been changed: ' + data_to_change + ' is not a valid json value'


@app.route('/api/ticket/add', methods=['POST'])
def ticket_add_new():
    """
    sequence diagram # 2
    """
    content = dict(request.get_json())

    pass


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


def get_user_data(content):
    username = content.get(json_keys.username)
    password = content.get(json_keys.password)
    level = content.get(json_keys.level)
    return username, password, level


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


drop_all_tables()
initialize_all_tables()
generate_test_db_data.generate(db, clear_existing=true)

if __name__ == '__main__':
    app.run()
