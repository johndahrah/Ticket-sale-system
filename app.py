import re

from flask import Flask
from sqlalchemy import *

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
db = create_engine(
    'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
    )


from handlers.TicketsHandler import tickets_handler
from handlers.UsersHandler import users_handler
from handlers.OrganizersHandler import organizers_handler
from handlers.CouponsHandler import coupons_handler
import StatisticsGenerator
app.register_blueprint(tickets_handler)
app.register_blueprint(users_handler)
app.register_blueprint(organizers_handler)
app.register_blueprint(coupons_handler)
app.register_blueprint(StatisticsGenerator.statistics_generator)


@app.route('/')
def test():
    # return render_template('organizers_list.html')
    return 'ok'


@app.route('/api/system/db/init_tables')
def initialize_all_tables():
    content = read_file('sql/create_tables.sql')
    return execute_sql_commands(content)


@app.route('/api/system/db/drop_tables')
def drop_all_tables():
    # todo: a good permission check is vital for this action
    content = read_file('sql/drop_all_tables.sql')
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


drop_all_tables()
initialize_all_tables()
generate_test_db_data.generate(db, clear_existing=true)

if __name__ == '__main__':
    app.run()
