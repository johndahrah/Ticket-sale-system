import requests
#
# res = requests.post(
#     'http://localhost:5000/api/user/modify', json={
#         "user_name": "user1",
#         "password": "999999999",
#         "privilege_level": "123",
#         "change": "--"
#     })

res = requests.post(
    'http://localhost:5000/api/ticket/add', json={
        "openedforselling": False,
        "eventdate": "999999999",
        "eventtime": "123",
        "eventplace": "--",
        "EventOrganizerName": "",
        "sellprice": 9999,
        "comment": "",
        "organizerid": "1",
        "serialnumber": "AAAAAA"

    })


print(res, res.content, sep='\n')
# ALWAYS make sure the request is sent in a correct URL address!
