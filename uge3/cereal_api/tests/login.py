import requests

url = 'http://localhost:81/login'
data = {'email': 'user@password.com', 'password': 'password'}

response = requests.post(url, data=data)

print(response.status_code)
print(response.cookies)
