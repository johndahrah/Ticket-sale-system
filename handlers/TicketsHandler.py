import datetime

from flask import request, Blueprint, render_template
from sqlalchemy.engine import ResultProxy
from sqlalchemy.exc import DataError, IntegrityError

import json_text_constants as j_const
from database import sql_abstract_builder as sql_bld, databaseProvider
from handlers import CouponsHandler

tickets_handler = Blueprint(
    'tickets_handler', __name__, url_prefix='/api/ticket'
    )
db = databaseProvider.connect_to_db()


@tickets_handler.route('/view/all', methods=['GET'])
def ticket_view_all():
    result_sys = db.execute(
        'SELECT * FROM tickets ORDER BY id'
        )
    result = [dict(row) for row in result_sys]
    return render_template('tickets_list.html', attributes=result)


@tickets_handler.route('/view', methods=['GET'])
def ticket_view_specific():
    if len(request.args) == 0:
        return ticket_view_all()

    sql_statement = sql_bld.build_select_with_multiple_conditions(
        table='tickets',
        parameters=j_const.all_ticket_properties,
        arguments=request.args
        )

    if sql_statement is not None:
        result_sys = db.execute(sql_statement)
        result = [dict(row) for row in result_sys]
        return render_template('tickets_list.html', attributes=result)
    else:
        return render_template(
            'tickets_list.html',
            error='Ошибка при выполнении запроса'
            )


@tickets_handler.route('/view/<ticket_id>')
def ticket_view_by_id(ticket_id):
    sql_statement = f'SELECT * FROM tickets ' \
                    f'WHERE id = {ticket_id}'
    result_sys = db.execute(sql_statement)
    result = [dict(row) for row in result_sys]
    return render_template('tickets_list.html', attributes=result)


@tickets_handler.route('/add', methods=['GET'])
def ticket_add():
    """
    required json: see column_names below
    """
    a = request.args
    sql_statement = f'SELECT * FROM tickets'
    result_sys = db.execute(sql_statement)
    result = [dict(row) for row in result_sys]
    try:
        sql_statement = f'SELECT name FROM organizers ' \
                        f'WHERE id = {int(a.get(j_const.organizerid))}'
        org_name = receive_sql_query_result(sql_statement)

        sql_statement = f'SELECT address FROM organizers ' \
                        f'WHERE id = {int(a.get(j_const.organizerid))}'
        address = receive_sql_query_result(sql_statement)
    except Exception:
        return render_template('tickets_list.html',
                               attributes=result,
                               error='Неверный ID организатора')

    amount = int(a.get('amount'))
    for i in range(1, amount+1):
        try:
            sql_statement = sql_bld.build_insert_of_single_entry(
                table='tickets',
                column_names=('openedForSelling', 'eventDate', 'eventTime',
                              'eventPlace', 'eventOrganizerName', 'sellPrice',
                              'comment', 'organizerID', 'serialNumber', 'isSold',
                              'eventName'),
                values=(False, str(a.get(j_const.date)),
                        str(a.get(j_const.time)), str(address),
                        str(org_name), a.get(j_const.price),
                        "",
                        str(a.get(j_const.organizerid)),
                        str(a.get(j_const.serial)) + str(i), False,
                        str(a.get(j_const.event_name)))
                )
        except KeyError as e:
            return f'Был получен невеный кллюч!'
        try:
            db.execute(sql_statement)
        except DataError:
            return f'Неверный тип данных'
        except IntegrityError as e:
            return f'Организатора с ID ' \
                   f'{int(a.get(j_const.organizerid))} не существует!'

    return render_template('tickets_list.html',
                           attributes=result,
                           success_message='Билет успешно добавлен')


def at_least_one_ticket_is_already_sold(tickets_id):
    sql_statement = f'SELECT * from tickets ' \
                    f'WHERE issold = TRUE '
    sql_statement += ' and '
    if type(tickets_id) is int:
        sql_statement += f'id = {tickets_id}'
    else:  # it is tuple
        sql_statement += f'id IN {tickets_id}'
    result = receive_sql_query_result(sql_statement)
    return result is not None


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
    """
    required json: sell_tickets_id (int or tuple), (coupon), userID
    """
    now = datetime.datetime.now()
    date = str(now.date())
    json = dict(request.json)
    coupon_data = json.get(j_const.coupon)
    if coupon_data == '':
        coupon_data = None

    # separate the cases of (only one) and (many) tickets being sold:
    # in case of one ticket, we operate with it as an "int"
    # in case of many tickets, we operate with them as a "tuple"
    tickets_ids = json.get(j_const.sell_tickets_id)
    if type(tickets_ids) is str:
        tickets_id = int(tickets_ids)
    else:
        tickets_id = tuple(tickets_ids)

    # checking request data validity.
    if at_least_one_ticket_is_already_sold(tickets_id):
        return 'Один (или более) билетов уже проданы'

    if at_least_one_ticket_is_closed_for_sale(tickets_id):
        return 'Один (или более) билетов закрыты для продажи'

    if coupon_data is not None and not CouponsHandler.is_valid(coupon_data):
        return 'Купон имеет неверный формат'

    username = json.get(j_const.username)
    if username == '':
        return 'Гостям запрещена продажа билетов'

    # insert the possible coupon data into the database
    if coupon_data is not None:
        sql_statement = sql_bld.build_insert_of_single_entry(
            table='coupons',
            column_names=('dateUsed', 'couponData'),
            values=(str(date), str(coupon_data))
            )
        db.execute(sql_statement)

    # mark necessary tickets as "sold"
    equal_operator = '=' if type(tickets_ids) is str else 'IN'
    sql_statement = f'UPDATE tickets ' \
                    f'SET issold = {True} ' \
                    f'WHERE id {equal_operator} {tickets_id}'
    db.execute(sql_statement)

    # receive the total price
    sql_statement = f'SELECT sum(sellprice) FROM tickets ' \
                    f'WHERE id {equal_operator} {tickets_id}'
    total_price = receive_sql_query_result(sql_statement)

    sql_statement = f'SELECT id FROM users ' \
                    f'WHERE login LIKE \'{username}\''
    worker_id = receive_sql_query_result(sql_statement)

    # receive coupon data
    sql_statement = f'SELECT id FROM coupons ' \
                    f'WHERE coupondata LIKE \'{coupon_data}\''
    coupon_id = receive_sql_query_result(sql_statement)

    # insert all data in "checks" table and receive the id of a new record
    sql_statement = sql_bld.build_insert_of_single_entry(
        table='checks',
        column_names=('TicketsAmount', 'TotalPrice',
                      'CouponUsed', 'CouponID', 'WorkerID'),
        values=(1 if type(tickets_ids) is str else len(tickets_id),
                total_price, coupon_data is not None,
                "null" if coupon_id is None else coupon_id,
                worker_id),
        returning_column='id'
        )
    check_id = receive_sql_query_result(sql_statement)

    # create a one-to-many relationship check<->ticket
    try:
        for ticket_id in tickets_id:
            sql_statement = sql_bld.build_insert_of_single_entry(
                table='check_ticketsid',
                values=(check_id, ticket_id)
                )
            db.execute(sql_statement)
    except TypeError:  # 'int' object is not iterable
        sql_statement = sql_bld.build_insert_of_single_entry(
            table='check_ticketsid',
            values=(check_id, tickets_id)
            )
        db.execute(sql_statement)
    return ''


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
    """
    required json: ticket_id, data_to_change
    """
    if not ticket_id_exists(ticket_id):
        return 'Билета с таким ID не существует'

    sql_statement = f'UPDATE tickets SET '

    json_dict = dict(request.get_json())
    if json_dict.get('id') is not None:
        return 'Вы не можете изменять ID билета'

    more_than_one_argument = False
    for i in j_const.all_ticket_properties:
        argument = json_dict.get(i)
        if argument is not None:
            if more_than_one_argument:
                sql_statement += ' , '
            if type(argument) is str and argument.upper() != 'NULL':
                sql_statement += f'{i} = \'{argument}\''
            else:
                sql_statement += f'{i} = {argument}'
            more_than_one_argument = True
    sql_statement += f' WHERE id = {ticket_id}'
    db.execute(sql_statement)
    return 'Успешно: билет изменен'


@tickets_handler.route('/delete/<ticket_id>', methods=['GET'])
def ticket_delete(ticket_id):
    if not ticket_id_exists(ticket_id):
        return 'Билета с таким ID не существует'
    sql_statement = f'DELETE FROM tickets ' \
                    f'WHERE id = {ticket_id}'
    try:
        db.execute(sql_statement)
    except IntegrityError:
        return 'Билет не может быть удален: в базе есть ссылающийся на него чек'

    return 'Успешно: билет удален'


def ticket_id_exists(ticket_id):
    sql_check_id_statement = f'SELECT * FROM tickets ' \
                             f'WHERE id = {ticket_id}'
    result_of_check: ResultProxy = db.execute(sql_check_id_statement)
    rows_number = result_of_check.rowcount
    return rows_number != 0
