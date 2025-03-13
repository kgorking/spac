import requests
import json

url = 'http://localhost:81/cereal/13'

response = requests.get(url)

print(response.status_code)
print(response.text)
#print(response.json())
