from flask import Blueprint, render_template, abort

from app import db

coupons_handler = Blueprint (
    'coupons_handler', __name__, url_prefix='/api/coupon'
    )


@coupons_handler.route('/view/all')
def coupons_view_all():
    result_sys = db.execute(
        'SELECT * FROM coupons'
        )
    result = [dict(row) for row in result_sys]
    return render_template('coupons_list.html', attributes=result)


@coupons_handler.route('/add')
def coupons_add():
    """
    coupons table is automatically updated on tickets_sell() method.
    todo: replace with @app.errorhandler()
    """
    return abort(405)


# don't @route anything here
# to avoid finding valid coupon via brute force
def is_valid(data: str):
    # something simple for now.
    # e.g.      7SAMPLE (valid)
    return len(data) == data[0]
