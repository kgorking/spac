import requests

url = 'http://localhost:81/cereal'
response = requests.get(url)

assert(200 == response.status_code)
assert(77 == len(response.json()))
