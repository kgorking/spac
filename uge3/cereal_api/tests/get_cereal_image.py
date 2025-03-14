from genericpath import exists
from os import remove
import requests

url = 'http://localhost:81/image/13'
response = requests.get(url)
assert(response.status_code == 200)

with open('downloaded_image.jpg', 'wb') as file:
    assert(0 < file.write(response.content))

# cleanup
if exists('downloaded_image.jpg'):
    remove('downloaded_image.jpg')
