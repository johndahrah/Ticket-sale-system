import requests

# res = requests.post(
#     'http://localhost:5000/api/user/add', json={
#         "user_name": "user199",
#         "password": "999999999",
#         "privilege_level": "123",
#     })

# res = requests.post(
#     'http://localhost:5000/api/ticket/add', json={
#         "openedforselling": False,
#         "eventdate": "999999999",
#         "eventtime": "123",
#         "eventplace": "--",
#         "EventOrganizerName": "",
#         "sellprice": 9999,
#         "comment": "",
#         "organizerid": "1",
#         "serialnumber": "AAAAAA"
#
#     })

# res = requests.get(
#     'http://localhost:5000/api/ticket/view?id=2')

# res = requests.post(
#     'http://localhost:5000/api/organizer/add', json={
#         "id": 99,
#         "name": "name 1",
#         "address": 'street A, 99'
#     })

#
# res = requests.get(
#     # 'http://localhost:5000/api/organizer/view?id=1')

res = requests.post(
    'http://localhost:5000/api/ticket/sell', json={
        "selling": (1, 2),
        "coupon": "AABBCC123",
        "userid": 1
    })


print(res, res.content, sep='\n')
# ALWAYS make sure the request is sent in a correct URL address!
