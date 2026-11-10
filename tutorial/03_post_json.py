"""
第 3 步：POST 一个 JSON body。

运行：
    python 03_post_json.py

你要看懂：
- requests.post(..., json=user) 会自动设置 Content-Type: application/json
- 创建后马上 GET 查询，确认真的创建成功
- 最后 DELETE 清理数据
"""

import time

import requests

BASE_URL = "https://petstore.swagger.io/v2"
username = f"qa_{int(time.time() * 1000)}"

user = {
    "id": 0,
    "username": username,
    "firstName": "QA",
    "lastName": "Test",
    "email": "qa@example.com",
    "password": "Passw0rd!",
    "phone": "13800000000",
    "userStatus": 1,
}

# 创建
r = requests.post(f"{BASE_URL}/user", json=user, timeout=20)
print("CREATE 状态码:", r.status_code)
print("CREATE 响应:", r.text)

# 查询
r = requests.get(f"{BASE_URL}/user/{username}", timeout=20)
print("GET 状态码:", r.status_code)
print("GET 响应:", r.text)

# 清理
r = requests.delete(f"{BASE_URL}/user/{username}", timeout=20)
print("DELETE 状态码:", r.status_code)
print("DELETE 响应:", r.text)
