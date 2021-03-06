import hashlib

users_data = [
    # username, password, access_level
    ('user1', hashlib.md5(b'12345').hexdigest(), 1),
    ('user2', hashlib.md5(b'pass123').hexdigest(), 1),
    ('admin', hashlib.md5(b'admin').hexdigest(), 2)
    ]

tickets_data = [
    {1: True,         # OpenedForSelling
     2: '18.08.2019',  # EventDate
     3: '19.00',       # EventTime
     4: 'Театральная пл., 1',    # EventPlace
     5: 'Большой театр',     # EventOrganizerName
     6: 1000,          # SellPrice
     7: '',            # Comment
     8: '1',           # OrganizerID
     9: 'ABC000',      # SerialNumberPrefix
     10: False,        # isSold
     11: 'Пиковая дама',     # eventName
     'amount': 20       # the amount of the tickets for this performance
                         # (not stored in the database)
     },

    {1: False,
     2: '01.04.2020',
     3: '18.00',
     4: 'Театральный проезд, д. 1',
     5: 'Малый театр',
     6: 1500,
     7: 'Вход до 17:30',
     8: '2',
     9: 'TIC',
     10: False,
     11: 'Сказка о царе Салтане',
     'amount': 10
     }
]

organizers_data = [
    # id, name, address
    ('1', 'Большой театр', 'Театральная пл., 1'),
    ('2', 'Малый театр', 'Театральный проезд, д. 1')
]


def generate(db, clear_existing=False):
    if clear_existing:
        db.execute(
            'DELETE FROM users; '
            'DELETE FROM tickets; '
            'DELETE FROM organizers'
        )

    for i in users_data:
        db.execute("INSERT INTO Users "
                   "(login, password, accessLevel) "
                   "VALUES (\'%s\', \'%s\', %s);"
                   % (i[0], i[1], i[2]))

    for i in organizers_data:
        db.execute("INSERT INTO organizers "
                   "(id, name, address) "
                   "VALUES (%s, \'%s\', \'%s\');"
                   % (i[0], i[1], i[2]))

    for i in tickets_data:
        for j in range(i.get('amount')):
            sql_statement = f'INSERT INTO tickets ' \
                            f'(OpenedForSelling, EventDate, EventTime, ' \
                            f'EventPlace, EventOrganizerName, SellPrice, ' \
                            f'Comment, OrganizerID, SerialNumber, isSold, ' \
                            f'eventName) ' \
                            f'VALUES (' \
                            f'{i[1]}, \'{i[2]}\', \'{i[3]}\', \'{i[4]}\', ' \
                            f'\'{i[5]}\', {i[6]}, \'{i[7]}\', \'{i[8]}\', ' \
                            f'\'{i[9] + str(j+1)}\', {j%5==0}, \'{i[11]}\'' \
                            f');'
            db.execute(sql_statement);
