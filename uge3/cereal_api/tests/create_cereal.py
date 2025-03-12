import requests

url = 'http://localhost:81/cereal'
data = {'name': 'Test cereal 2'}

response = requests.post(url, json=data)

print(response.status_code)
#print(response.text)
print(response.json())
