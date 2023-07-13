import requests

endpoint = 'http://localhost:8000/api/'

response = requests.post(endpoint, data={'title': 'Hello World!'})

print(response.json())
