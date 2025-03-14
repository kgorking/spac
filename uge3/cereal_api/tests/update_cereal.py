import requests

url = 'http://localhost:81/api/login'
data = {'email': 'user@password.com', 'password': 'password'}
login_response = requests.post(url, data=data)
assert(200 == login_response.status_code)

url = 'http://localhost:81/api/cereal/update'
data = {'id': 78, 'name': 'Test cereal 3'}
response = requests.post(url, json=data, cookies=login_response.cookies)
assert(200 == response.status_code)
assert(1 == response.json()['num_rows_updated'])

url = 'http://localhost:81/api/cereal/78'
response = requests.get(url)
assert(200 == response.status_code)
assert(data['name'] == response.json()['name'])
