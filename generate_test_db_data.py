users_data = [
    # username, password, access_level
    ('user1', '12345', 1),
    ('user2', 'pass123', 1),
    ('manager1', 'secret_pass', 2)
]

tickets_data = [
    {'1': False,         # OpenedForSelling
     '2': '18.08.2019',  # EventDate
     '3': '19.00',       # EventTime
     '4': 'Street 1',    # EventPlace
     '5': 'Theatre',     # EventOrganizerName
     '6': 1000,          # SellPrice
     '7': '',            # Comment
     '8': '1',           # OrganizerID
     'amount': 100       # the amount of the tickets for this performance
                         # (not stored in the database)
     },

    {'1': True,
     '2': '01.04.2020',
     '3': '18.00',
     '4': 'Street 2',
     '5': 'Theatre 2',
     '6': 1500,
     '7': 'Enter before 17:30',
     '8': '2',
     'amount': 50
     }
]

organizers_data = [
    # id, name, address
    ('1', 'Theatre 1', 'Street 1'),
    ('2', 'Theatre 2', 'Street 2')
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
            db.execute(
                "INSERT INTO tickets "
                "(OpenedForSelling, EventDate, EventTime, EventPlace, "
                "EventOrganizerName, SellPrice, Comment, OrganizerID)"
                "VALUES (%(1)r, \'%(2)s\', \'%(3)s\', \'%(4)s\', \'%(5)s\', %(6)s, \'%(7)s\', \'%(8)s\');" % i
            )
