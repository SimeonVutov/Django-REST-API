import requests

endpoint = 'https://httpbin.org/anything'

response = requests.get(endpoint, json={'query': 'Hello World!'})

print(response.text)
print(response.json())