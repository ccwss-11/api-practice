"""
11.18 任务：用 Python requests 完成
创建用户 -> 登录 -> 查询 -> 删除 -> 再查 404
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

# 1. 用 Session 复用 headers/连接
session = requests.Session()
session.headers.update({"Accept": "application/json"})

# 2. 创建用户
r = session.post(f"{BASE_URL}/user", json=user, timeout=20)
print("CREATE:", r.status_code, r.text)
assert r.status_code == 200
assert r.json()["code"] == 200

# 3. 登录
r = session.get(
    f"{BASE_URL}/user/login",
    params={"username": USERNAME, "password": PASSWORD},
    timeout=20,
)
print("LOGIN:", r.status_code, r.text)
assert r.status_code == 200
assert "logged in user session" in r.json()["message"]

# 4. 查询
r = session.get(f"{BASE_URL}/user/{USERNAME}", timeout=20)
print("GET:", r.status_code, r.text)
assert r.status_code == 200
assert r.json()["username"] == USERNAME

# 5. 删除
r = session.delete(f"{BASE_URL}/user/{USERNAME}", timeout=20)
print("DELETE:", r.status_code, r.text)
assert r.status_code == 200

# 6. 再查，确认 404
r = session.get(f"{BASE_URL}/user/{USERNAME}", timeout=20)
print("GET_AFTER_DELETE:", r.status_code, r.text)
assert r.status_code == 404

session.close()
print("DONE")
