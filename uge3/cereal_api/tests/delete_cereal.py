import requests

url = 'http://localhost:81/api/login'
data = {'email': 'user@password.com', 'password': 'password'}
login_response = requests.post(url, data=data)
assert(200 == login_response.status_code)

url = 'http://localhost:81/api/cereal/delete/78'
response = requests.delete(url, cookies=login_response.cookies)
assert(200 == response.status_code)
