import requests

endpoint = 'http://127.0.0.1:8000/api/products/create/'

response = requests.post(endpoint, params={'abc': 123}, json={"title": "Product 1"})
print(response.json())