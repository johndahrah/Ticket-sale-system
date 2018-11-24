from sqlalchemy import create_engine
import os


def connect_to_db():
    try:
        url = os.environ['DATABASE_URL']
    except KeyError:
        url = None

    if url is not None:
        return create_engine(url)

    data = {
        'user': 'postgres',
        'pw': '1234',
        'db': 'postgres',
        'host': 'localhost',
        'port': '5432',
        }
    return create_engine(
        'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % data
        )
