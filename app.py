import re

from flask import Flask, render_template
from sqlalchemy import *
import os

from database import generate_test_db_data, databaseProvider
from handlers.StatisticsGenerator import statistics_generator
from handlers.CouponsHandler import coupons_handler
from handlers.OrganizersHandler import organizers_handler
from handlers.TicketsHandler import tickets_handler
from handlers.UsersHandler import users_handler
from handlers.ChecksHandler import checks_handler

app = Flask(__name__)
db = databaseProvider.connect_to_db()


app.register_blueprint(tickets_handler)
app.register_blueprint(users_handler)
app.register_blueprint(organizers_handler)
app.register_blueprint(coupons_handler)
app.register_blueprint(statistics_generator)
app.register_blueprint(checks_handler)


@app.route('/')
def init():
    return render_template('start_page.html')


@app.route('/api/system/db/init_tables')
def initialize_all_tables():
    content = read_file('database/sql/create_tables.sql')
    return execute_sql_commands(content)


@app.route('/api/system/db/drop_tables')
def drop_all_tables():
    # todo: a good permission check is vital for this action
    content = read_file('database/sql/drop_all_tables.sql')
    return execute_sql_commands(content)


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


@app.route('/favicon.ico')
def send_favicon():
    return ''


@app.route('/api/system/revert')
def revert():
    rebuild_tables()
    return render_template('start_page.html')


def rebuild_tables():
    drop_all_tables()
    initialize_all_tables()
    generate_test_db_data.generate(db, clear_existing=true)


rebuild_tables()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
