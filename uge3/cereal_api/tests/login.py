import requests

url = 'http://localhost:81/login'
data = {'email': 'user@password.com', 'password': 'password'}

response = requests.post(url, data=data)
assert(200 == response.status_code)
