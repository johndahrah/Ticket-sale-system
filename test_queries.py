import requests

res = requests.post(
    'http://localhost:5000/api/user/add', json={
        "user_name": "test_name",
        "password": "12345",
        "level": "cashier"
    })

print(res)