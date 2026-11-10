import requests

r = requests.get(
    "https://petstore.swagger.io/v2/store/inventory",
    timeout=20
)
print(r.status_code)
print(r.text[:200])