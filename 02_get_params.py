import requests

r = requests.get(
    "https://petstore.swagger.io/v2/pet/findByStatus",
    params={"status": "available"},
    timeout=20,
)

print("最终 URL:", r.url)
print("数量:", len(r.json()))