import requests

url = 'http://localhost:81/api/cereal?select=name,fiber'
response = requests.get(url)
assert(200 == response.status_code)

# Check selects
for cereal in response.json():
    assert('name' in cereal)
    assert('fiber' in cereal)
    assert('fat' not in cereal)
