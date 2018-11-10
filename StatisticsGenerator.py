from flask import Blueprint, abort
from sqlalchemy import exc

from app import db

statistics_generator = Blueprint(
    'statistics_generator', __name__, url_prefix='/api/stat'
    )


@statistics_generator.route('/tickets')
def generate_tickets_statistics():
    sql_statement = f'SELECT * FROM tickets'

    try:
        result_sys = db.execute(sql_statement)
    except exc.IntegrityError:
        return 'table tickets dies not exist!'

    result = [dict(row) for row in result_sys]

    total_price_of_sold = 0
    for i in result:
        if i.get('issold'):
            total_price_of_sold += i.get('sellprice')

    return str(total_price_of_sold)


@statistics_generator.route('/coupons')
def generate_coupons_statistics():
    sql_statement = f'SELECT * FROM coupons'

    result_sys = db.execute(sql_statement)
    result = [dict(row) for row in result_sys]

    coupons_usage_distribution = {}
    return abort(501)  # for now
