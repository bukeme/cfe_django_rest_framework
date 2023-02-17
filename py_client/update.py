import requests

endpoint = 'http://127.0.0.1:8000/api/products/5/update/'

response = requests.put(endpoint, json={"title": "My Updated Product While Trying Mixins", "price": 40.00})
print(response.json())