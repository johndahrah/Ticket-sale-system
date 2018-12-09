from flask import Blueprint
from database import databaseProvider

checks_handler = Blueprint (
    'checks_handler', __name__, url_prefix='/api/check'
    )
db = databaseProvider.connect_to_db()


@checks_handler.route('/view/all')
def checks_view_all():
    result_sys = db.execute(
        'SELECT * FROM checks ORDER BY id'
        )
    result = [dict(row) for row in result_sys]
    out = ''
    for i in result:
        out += '<br/>'.join([f'{key}: {value}'
                             for (key, value) in i.items()])
        out += '<br/> <br/>'
    return out
