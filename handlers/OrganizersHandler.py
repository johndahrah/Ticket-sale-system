from flask import request, Blueprint, jsonify
from sqlalchemy import engine

import json_text_constants as j_const
from app import db

organizers_handler = Blueprint(
    'organizers_handler', __name__, url_prefix='/api/organizer'
    )


@organizers_handler.route('/view/all')
def organizers_view_all():
    result = db.execute(
        'SELECT * FROM organizers'
        )
    return jsonify({'result': [dict(row) for row in result]})


@organizers_handler.route('/view/<organizer_id>')
def organizer_view_specific(organizer_id):
    if len(request.args) == 0:
        return organizers_view_all()
    pass


@organizers_handler.route('/add', methods=['POST'])
def organizer_add():
    content = dict(request.get_json())
    organizer_id, name, address = get_organizer_data(content)
    if not_exists(organizer_id):
        sql_statement = f'INSERT INTO organizers ' \
                        f'VALUES (' \
                        f'{organizer_id}, \'{name}\', \'{address}\'' \
                        f')'
        db.execute(sql_statement)
        return 'ok'
    else:
        return 'organizer with such id already exists!'


def not_exists(organizer_id):
    sql_statement = f'SELECT * FROM organizers ' \
                    f'WHERE ID = {organizer_id}'
    result: engine.ResultProxy = db.execute(sql_statement)
    return result.rowcount == 0


def get_organizer_data(content):
    name = content.get(j_const.organizer_name)
    address = content.get(j_const.organizer_address)
    organizer_id = content.get(j_const.organizer_id)
    return organizer_id, name, address

