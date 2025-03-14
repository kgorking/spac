import requests

url = 'http://localhost:81/api/cereal?sort=fat'
response = requests.get(url)
assert(200 == response.status_code)

# Check sorting
fat: int = -1
for cereal in response.json():
    assert(fat <= cereal['fat'])
    fat = cereal['fat']
