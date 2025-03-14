import requests

# This filter has 1 cereal match
url = 'http://localhost:81/cereal?fiber=3.0&fat=1&carbo=15.0'
response = requests.get(url)

assert(200 == response.status_code)
assert(1 == len(response.json()))
