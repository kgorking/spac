import requests

url = 'http://localhost:81/cereal/create'
data = {'name': 'Test cereal 2', 'mfr': 'C', 'type': 'test'}

response = requests.post(url, json=data)

print(response.status_code)
#print(response.text)
print(response.json())
