import requests
import json

url = 'http://localhost:81/cereal'

response = requests.get(url)

print(response.status_code)
print(response.json())
