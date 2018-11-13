from flask import request, Blueprint, render_template, redirect, url_for

import databaseProvider
import json_text_constants as j_const
import sql_abstract_builder as sql_bld

users_handler = Blueprint(
    'users_handler', __name__, url_prefix='/api/user'
    )
db = databaseProvider.connect_to_db()


@users_handler.route('/add', methods=['POST'])
def user_add():
    content = dict(request.get_json())
    username, password, level = get_user_data(content)

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


@users_handler.route('/api/users/login')
def login():
    if request.args.get('asGuest') is not None:
        return redirect(url_for('tickets_handler.ticket_view_specific'))

    username = request.args.get('username')
    password = request.args.get('password')
    sql_statement = f'SELECT * FROM users ' \
                    f'WHERE login LIKE \'{username}\' ' \
                    f'AND password LIKE \'{password}\''
    if receive_sql_query_result(sql_statement) is not None:
        return redirect(url_for('tickets_handler.ticket_view_specific'))
    else:
        return render_template('start_page.html',
                               error='Неверное имя пользователя или пароль ')


def receive_sql_query_result(sql_statement):
    """
    works only for receiving a single variable.
    """
    sql_sum_result = db.execute(sql_statement)
    result = []
    for row in sql_sum_result:
        result.append(row)

    try:
        data = result[0]._row[0]
    except IndexError:
        return None
    return data
