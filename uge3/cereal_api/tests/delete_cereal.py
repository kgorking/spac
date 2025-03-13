import requests

url = 'http://localhost:81/login'
data = {'email': 'user@password.com', 'password': 'password'}
login_response = requests.post(url, data=data)

url = 'http://localhost:81/cereal/delete/78'
response = requests.delete(url, cookies=login_response.cookies)

print(response.status_code)
print(response.json())
