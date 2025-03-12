import requests

url = 'http://localhost:81/cereal'
data = {'id': 78}

response = requests.delete(url, json=data)

print(response.status_code)
print(response.json())
