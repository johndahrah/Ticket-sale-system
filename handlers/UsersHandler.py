from flask import request, Blueprint

import json_text_constants as j_const
from app import db
import sql_abstract_builder as sql_bld

users_handler = Blueprint(
    'users_handler', __name__, url_prefix='/api/user'
    )


@users_handler.route('/add', methods=['POST'])
def user_add():
    content = dict(request.get_json())
    username, password, level = get_user_data(content)

    # db.execute(
    #     "INSERT INTO Users "
    #     "(login, password, accessLevel) "
    #     "VALUES (\'%s\', \'%s\', %s);"
    #     % (username, password, level)
    #     )
    sql_statement = sql_bld.build_insert_of_single_entry(
        table='users',
        column_names=('login', 'password', 'accessLevel'),

        # explicitly set the types of username and password
        # to 'str', as they are considered as 'Any' before.
        values=(str(username), str(password), level),
        )
    db.execute(sql_statement)
    return 'ok'


@users_handler.route('/modify', methods=['GET', 'POST'])
def user_modify():
    # todo check if the user is in the database
    content = dict(request.get_json())
    username, password, level = get_user_data(content)
    data_to_change = content.get(j_const.change_data_type)

    if data_to_change == j_const.level:
        db.execute(
            f'UPDATE users SET accesslevel = {level} '
            f'WHERE login LIKE \'{username}\''
            )
        return 'ok'
    if data_to_change == j_const.password:
        db.execute(
            f'UPDATE users SET password = {password} '
            f'WHERE login LIKE \'{username}\''
            )
        return 'ok'
    if data_to_change == j_const.username:
        # todo username change
        pass
    return j_const.json_change_value_error % data_to_change


def get_user_data(content):
    username = content.get(j_const.username)
    password = content.get(j_const.password)
    level = content.get(j_const.level)
    return username, password, level