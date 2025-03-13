import requests

url = 'http://localhost:81/cereal?fiber=3.0&fat=1&carbo=15.0'

response = requests.get(url)

print(response.status_code)
print(response.json())
