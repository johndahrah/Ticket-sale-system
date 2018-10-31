import datetime

from flask import jsonify, request, Blueprint
from sqlalchemy.engine import ResultProxy
from sqlalchemy.exc import DataError

import json_text_constants as j_const
from app import db

tickets_handler = Blueprint(
    'tickets_handler', __name__, url_prefix='/api/ticket'
    )


@tickets_handler.route('/view/all', methods=['GET'])
def ticket_view_all():
    result = db.execute(
        'SELECT * FROM tickets'
        )
    return jsonify({'result': [dict(row) for row in result]})


@tickets_handler.route('/view', methods=['GET'])
def ticket_view_specific():
    if len(request.args) == 0:
        return ticket_view_all()

    sql_statement = 'SELECT * FROM tickets'
    # the following line is for preventing IDE from "unexpected eol" warning
    sql_statement += ' WHERE '
    multiple_parameters = False
    at_least_one_argument = False
    for json_key in j_const.all_properties:
        argument = request.args.get(json_key)
        if argument is not None:
            at_least_one_argument = True
            equal_operator = '=' if argument.isdigit() else 'LIKE'
            if multiple_parameters:
                sql_statement += ' AND '
            sql_statement += f'{json_key} {equal_operator} {argument}'
            multiple_parameters = True
    if at_least_one_argument:
        result = db.execute(sql_statement)
        return jsonify({'result': [dict(row) for row in result]})
    else:
        return 'no one correct json key found'


@tickets_handler.route('/view/<ticket_id>')
def ticket_view_by_id(ticket_id):
    sql_statement = f'SELECT * FROM tickets ' \
                    f'WHERE id = {ticket_id}'
    result = db.execute(sql_statement)
    return jsonify({'result': [dict(row) for row in result]})


@tickets_handler.route('/add', methods=['GET', 'POST'])
def ticket_add():
    i = dict(request.get_json())
    try:
        sql_statement = f'INSERT INTO tickets ' \
                        f'(OpenedForSelling, EventDate, EventTime, ' \
                        f'EventPlace, EventOrganizerName, SellPrice, ' \
                        f'Comment, OrganizerID, SerialNumber, isSold) ' \
                        f'VALUES (' \
                        f'{i[j_const.opened]}, ' \
                        f'\'{i[j_const.date]}\', ' \
                        f'\'{i[j_const.time]}\', ' \
                        f'\'{i[j_const.place]}\', ' \
                        f'\'{i[j_const.organizer]}\', ' \
                        f'{i[j_const.price]}, ' \
                        f'\'{i[j_const.comment]}\', ' \
                        f'\'{i[j_const.organizerid]}\', ' \
                        f'\'{i[j_const.serial]}\', {False}' \
                        f');'
    except KeyError as e:
        return f'invalid json key has been received, check: {e}'
    try:
        db.execute(sql_statement)
    except DataError as e:
        return f'invalid type! Details: {e}'
    return 'successful'


def at_least_one_ticket_is_already_sold(tickets_id):
    # todo: implement
    return False


def at_least_one_ticket_is_closed_for_sale(tickets_id):
    try:
        for i in tickets_id:
            sql_statement = f'SELECT * FROM tickets ' \
                            f'WHERE id = {i} AND openedforselling = true'
            result = receive_sql_query_result(sql_statement)
            if result is None:
                return True
        return False
    except TypeError:  # 'int' object is not iterable
        sql_statement = f'SELECT * FROM tickets ' \
                        f'WHERE id = {tickets_id} AND openedforselling = true'
        result = receive_sql_query_result(sql_statement)
        return result is None


@tickets_handler.route('/sell', methods=['POST'])
def ticket_sell():
    now = datetime.datetime.now()
    date = str(now.date())
    json = dict(request.json)
    coupon_data = json.get(j_const.coupon)

    # separate the cases of (only one) and (many) tickets being sold:
    #  in case of one ticket, we operate with it as an "int"
    #  in case of many tickets, we operate with them as a "tuple"
    tickets_ids = json.get(j_const.sell_tickets_id)
    if type(tickets_ids) is int:
        tickets_id = tickets_ids
    else:
        tickets_id = tuple(json.get(j_const.sell_tickets_id))

    if at_least_one_ticket_is_already_sold(tickets_id):
        return 'One or more chosen tickets are already sold'

    if at_least_one_ticket_is_closed_for_sale(tickets_id):
        return 'One or more chosen tickets are closed for sale'

    # insert the possible coupon data into the database
    if coupon_data is not None:
        sql_statement = f'INSERT INTO coupons ' \
                        f'(dateUsed, couponData) ' \
                        f'VALUES (\'{date}\', \'{coupon_data}\')'
        db.execute(sql_statement)

    # mark necessary tickets as "sold"
    equal_operator = '=' if type(tickets_ids) is int else 'IN'
    sql_statement = f'UPDATE tickets ' \
                    f'SET issold = {True} ' \
                    f'WHERE id {equal_operator} {tickets_id}'
    db.execute(sql_statement)

    # receive the total price
    sql_statement = f'SELECT sum(sellprice) FROM tickets ' \
                    f'WHERE id {equal_operator} {tickets_id}'
    total_price = receive_sql_query_result(sql_statement)

    worker_id = json.get(j_const.userID)

    # receive coupon data
    sql_statement = f'SELECT id FROM coupons ' \
                    f'WHERE coupondata LIKE \'{coupon_data}\''
    coupon_id = receive_sql_query_result(sql_statement)

    # insert all data in "checks" table and receive the id of a new record
    sql_statement = f'INSERT INTO checks ' \
                    f'(TicketsAmount, TotalPrice, ' \
                    f'CouponUsed, CouponID, WorkerID) ' \
                    f'VALUES (' \
                    f'{1 if type (tickets_ids) is int else len(tickets_id)},' \
                    f'{total_price}, {coupon_data is not None}, ' \
                    f'{"null" if coupon_id is None else coupon_id}, ' \
                    f'{worker_id}) ' \
                    f'RETURNING id'
    check_id = receive_sql_query_result(sql_statement)

    # create a one-to-many relationship check<->ticket
    try:
        for ticket_id in tickets_id:
            sql_statement = f'INSERT INTO check_ticketsid VALUES ' \
                            f'({check_id}, {ticket_id})'
            db.execute(sql_statement)
    except TypeError:  # 'int' object is not iterable
        sql_statement = f'INSERT INTO check_ticketsid VALUES ' \
                        f'({check_id}, {tickets_id})'
        db.execute(sql_statement)
    return 'ok'


def receive_sql_query_result(sql_statement):
    """
    works only for receiving a single variable.
    """
    sql_sum_result: ResultProxy = db.execute(sql_statement)
    result = []
    if sql_sum_result.rowcount != 1:
        print('--- CHECK receive_sql_query_result ---')
    for row in sql_sum_result:
        result.append(row)

    try:
        data = result[0]._row[0]
    except IndexError:
        return None
    return data


@tickets_handler.route('/modify/<ticket_id>', methods=['GET', 'POST'])
def ticket_modify(ticket_id):
    if not ticket_id_exists(ticket_id):
        return 'no ticket with such ID'

    sql_statement = f'UPDATE tickets SET '

    json_dict = dict(request.get_json())
    if json_dict.get('id') is not None:
        return 'you can not modify ticket\'s ID'

    more_than_one_argument = False
    for i in j_const.all_properties:
        argument = json_dict.get(i)
        if argument is not None:
            if more_than_one_argument:
                sql_statement += ' , '
            sql_statement += f'{i} = {argument}'
            more_than_one_argument = True
    sql_statement += f'WHERE id = {ticket_id}'
    db.execute(sql_statement)
    return 'ok'


def ticket_id_exists(ticket_id):
    sql_check_id_statement = f'SELECT * FROM tickets ' \
                             f'WHERE id = {ticket_id}'
    result_of_check: ResultProxy = db.execute(sql_check_id_statement)
    rows_number = result_of_check.rowcount
    return rows_number != 0
