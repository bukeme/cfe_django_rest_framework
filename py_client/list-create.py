import requests

# endpoint = 'http://127.0.0.1:8000/api/products/list-create/'

# response = requests.get(endpoint)
# print(response.json())


# endpoint = 'http://127.0.0.1:8000/api/products/list-create/'

# response = requests.post(endpoint, params={'abc': 123}, json={"title": "Product 1"})
# print(response.json())

auth_endpoint = 'http://127.0.0.1:8000/api/auth/'

response = requests.post(auth_endpoint, json={"username": "staff", "password": "testing321"})
print(response.json())

endpoint = 'http://127.0.0.1:8000/api/products/list-create/'

if response.status_code == 200:
    token = response.json()['token']
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(endpoint, headers=headers)
    print(response.json())
