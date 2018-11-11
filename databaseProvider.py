from sqlalchemy import create_engine


def connect_to_db():
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
