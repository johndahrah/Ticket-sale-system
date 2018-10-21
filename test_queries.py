import requests

res = requests.post(
    'http://localhost:5000/api/user/modify', json={
        "user_name": "user1",
        "password": "999999999",
        "privilege_level": "123",
        "change": "--"
    })

print(res, res.content, sep='\n')
# ALWAYS make sure the request is sent in a correct URL address!
