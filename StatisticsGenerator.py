from flask import Blueprint
from sqlalchemy import exc


statistics_generator = Blueprint(
    'statistics_generator', __name__, url_prefix='/api/stat'
    )

from app import db


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

    stat = [coupons_data_usage_distribution, coupons_date_usage_distribution]
    return str(stat)
