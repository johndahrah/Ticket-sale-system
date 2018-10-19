import requests

res = requests.post(
    'http://localhost:5000/api/user/add', json={
        "user_name": "namexyz",
        "password": "12345",
        "privilege_level": "1"
    })

print(res)