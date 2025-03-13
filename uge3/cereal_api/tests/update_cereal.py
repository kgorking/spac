import requests

url = 'http://localhost:81/login'
data = {'email': 'user@password.com', 'password': 'password'}
login_response = requests.post(url, data=data)

url = 'http://localhost:81/cereal/update'
data = {'id': 78, 'name': 'Test cereal 3'}
response = requests.post(url, json=data, cookies=login_response.cookies)

print(response.status_code)
print(response.json())
