import requests

url = 'http://localhost:81/api/cereal/13'
response = requests.get(url)

assert(200 == response.status_code)
assert(17 == len(response.json())) # holds each column
