import requests
import json

url = 'http://localhost:81/image/1333'
response = requests.get(url)

if response.status_code == 200:
    with open('downloaded_image.jpg', 'wb') as file:
        file.write(response.content)
    print("Image saved successfully!")
else:
    print("Failed to retrieve the image.")
