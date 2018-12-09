from flask import Blueprint
from sqlalchemy import exc

from database import databaseProvider

statistics_generator = Blueprint(
    'statistics_generator', __name__, url_prefix='/api/stat'
    )
db = databaseProvider.connect_to_db()


@statistics_generator.route('/tickets')
def generate_tickets_statistics():
    result = {}

    sql_statement = f'SELECT count(*) FROM tickets'
    value = receive_sql_query_result(sql_statement)
    result['total_tickets_amount'] = value

    sql_statement = f'SELECT sum(sellprice) FROM tickets'
    value = receive_sql_query_result(sql_statement)
    result['total_sum'] = value

    sql_statement = f'SELECT sum(sellprice) FROM tickets ' \
                    f'where issold = TRUE'
    value = receive_sql_query_result(sql_statement)
    result['total_sold_sum'] = value

    return '<br/>'.join([f'{key}: {value}'for (key, value) in result.items()])


@statistics_generator.route('/coupons')
def generate_coupons_statistics():
    sql_statement = f'SELECT * FROM coupons'

    result_sys = db.execute(sql_statement)
    result = [dict(row) for row in result_sys]

    coupons_data_usage_distribution = dict()
    coupons_date_usage_distribution = dict()
    for i in result:
        data = i.get('coupondata')
        date = i.get('dateused')
        if data in coupons_data_usage_distribution:
            coupons_data_usage_distribution[data] += 1
        else:
            coupons_data_usage_distribution[data] = 1

        if date in coupons_date_usage_distribution:
            coupons_date_usage_distribution[date] += 1
        else:
            coupons_date_usage_distribution[date] = 1

    stat = [
        '<br/>'.join([f'{key}: {value}' for (key, value) in
                      coupons_data_usage_distribution.items()]),
        '<br/>'.join([f'{key}: {value}' for (key, value) in
                      coupons_date_usage_distribution.items()])]
    return str(stat)


@statistics_generator.route('/all')
def show_all_statistics():
    return f'{generate_tickets_statistics()} <br> ' \
           f'{generate_coupons_statistics()}'


def receive_sql_query_result(sql_statement):
    """
    works only for receiving a single variable.
    """
    sql_sum_result = db.execute(sql_statement)
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
