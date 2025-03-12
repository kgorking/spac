import requests

url = 'http://localhost:81/cereal'
data = {'id': 79, 'name': 'Test cereal 3'}

response = requests.post(url, json=data)

print(response.status_code)
print(response.json())
