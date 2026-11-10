"""
第 4 步：用 Session 串起完整链路。

运行：
    python 04_session_flow.py

你要看懂：
- requests.Session() 复用 headers 和连接
- 创建 -> 登录 -> 查询 -> 删除 -> 再查 404
- 每一步都检查 status_code
"""

import time

import requests

BASE_URL = "https://petstore.swagger.io/v2"
USERNAME = f"qa_{int(time.time() * 1000)}"
PASSWORD = "Passw0rd!"

user = {
    "id": 0,
    "username": USERNAME,
    "firstName": "QA",
    "lastName": "Test",
    "email": "qa@example.com",
    "password": PASSWORD,
    "phone": "13800000000",
    "userStatus": 1,
}

session = requests.Session()
session.headers.update({"Accept": "application/json"})

# 1. 创建
r = session.post(f"{BASE_URL}/user", json=user, timeout=20)
print("CREATE:", r.status_code, r.text)
assert r.status_code == 200
assert r.json()["code"] == 200

# 2. 登录
r = session.get(
    f"{BASE_URL}/user/login",
    params={"username": USERNAME, "password": PASSWORD},
    timeout=20,
)
print("LOGIN:", r.status_code, r.text)
assert r.status_code == 200
assert "logged in user session" in r.json()["message"]

# 3. 查询
r = session.get(f"{BASE_URL}/user/{USERNAME}", timeout=20)
print("GET:", r.status_code, r.text)
assert r.status_code == 200
assert r.json()["username"] == USERNAME

# 4. 删除
r = session.delete(f"{BASE_URL}/user/{USERNAME}", timeout=20)
print("DELETE:", r.status_code, r.text)
assert r.status_code == 200

# 5. 再查，确认 404
r = session.get(f"{BASE_URL}/user/{USERNAME}", timeout=20)
print("GET_AFTER_DELETE:", r.status_code, r.text)
assert r.status_code == 404

session.close()
print("DONE")
