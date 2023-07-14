import requests

endpoint = 'http://localhost:8000/api/products/1/update/'

data = {
    'title': 'Hello World from the updated product',
    'price': 1000
}

response = requests.put(endpoint, json=data)

print(response.json())
