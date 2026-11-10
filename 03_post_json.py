import requests

user = {
    "username": "qa_test_001",
    "firstName": "QA",
    "lastName": "Test",
    "email": "qa@example.com",
    "password": "Passw0rd!",
}

r = requests.post(
    "https://petstore.swagger.io/v2/user",
    json=user,
    timeout=20,
)

print(r.status_code)
print(r.text)