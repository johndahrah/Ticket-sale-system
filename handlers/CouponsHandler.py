from flask import Blueprint, render_template, abort
from sqlalchemy import exc

from database import databaseProvider

coupons_handler = Blueprint (
    'coupons_handler', __name__, url_prefix='/api/coupon'
    )
db = databaseProvider.connect_to_db()


@coupons_handler.route('/view/all')
def coupons_view_all():
    sql_statement = 'SELECT * FROM coupons'
    try:
        result_sys = db.execute(sql_statement)
    except exc.ProgrammingError:
        return abort(
            500,
            description=f'Error happened while executing {sql_statement}'
            )
    result = [dict(row) for row in result_sys]
    return render_template('coupons_list.html', attributes=result)


@coupons_handler.route('/add')
def coupons_add():
    return abort(405, description="""
    Coupons is automatically created when tickets sell action
    is called, so you don't have to create one before purchasing.
    """)


@coupons_handler.route('/check/<data>')
def coupon_check_validity(data: str):
    if is_valid(data):
        return 'Купон может быть применен'
    else:
        return 'Купон имеет неверный формат'


def is_valid(data: str):
    # something simple for now.
    # e.g.      7SAMPLE (valid)

    if data is None:
        return False
    if not data[0].isdigit():
        return False
    if len(data) != int(data[0]):
        return False
    return True


def get_discount_amount(data: str=None):
    if is_valid(data):
        return int(data[0])
    else:
        return 0
