import requests

url = 'http://localhost:81/api/login'
data = {'email': 'user@password.com', 'password': 'password'}
login_response = requests.post(url, data=data)
assert(200 == login_response.status_code)

url = 'http://localhost:81/api/cereal/create'
data = {'name': 'Test cereal 2', 'mfr': 'C', 'type': 'test'}
response = requests.post(url, json=data, cookies=login_response.cookies)
assert(201 == response.status_code)
assert(78 == response.json()['id'])
