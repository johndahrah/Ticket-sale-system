import requests

res = requests.post(
    'http://localhost:5000/api/json_example', json={
        "test_attribute": "test_value"
    })

print(res)
if res.ok:
    print(res.json())