import requests

url = 'http://localhost:81/cereal/delete/78'

response = requests.delete(url)

print(response.status_code)
print(response.json())
