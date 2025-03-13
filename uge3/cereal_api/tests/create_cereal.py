import requests

url = 'http://localhost:81/login'
data = {'email': 'user@password.com', 'password': 'password'}
login_response = requests.post(url, data=data)

url = 'http://localhost:81/cereal/create'
data = {'name': 'Test cereal 2', 'mfr': 'C', 'type': 'test'}
response = requests.post(url, json=data, cookies=login_response.cookies)

print(response.status_code)
print(response.text)
#print(response.json())
