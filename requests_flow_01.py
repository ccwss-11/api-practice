import requests
import time
BASE_URL = "https://petstore.swagger.io/v2"
USERNAME = f"qa_{int(time.time() * 1000)}"
PASSWORD = "password"
user = {
    "id": 1,
    "username": f"{USERNAME}",
    "firstName": "QA",
    "lastName": "Test",
    "email": "qa@example.com",
    "password": "Passw0rd!",
    "phone": "13800000000",
    "userStatus": 1
}
# 初始化session
session = requests.Session()
session.headers.update({"accept": "application/json","api_key": "special-key"})

# 创建用户
r = session.post(f"{BASE_URL}/user",json=user, timeout=20)
print("CREATE:", r.status_code, r.text)
assert r.status_code == 200
assert r.json()["code"] == 200
# 登录
r = session.get(
    f"{BASE_URL}/user/login",
    params={"username": USERNAME, "password": PASSWORD},
    timeout=20
)
print("LOGIN:", r.status_code, r.text)
assert r.status_code == 200
assert "logged in user session" in r.json()["message"]
# 查询用户
r = session.get(f"{BASE_URL}/user/{USERNAME}", timeout=20)
print("GET:", r.status_code, r.text)
assert r.status_code == 200
assert r.json()["username"] == USERNAME
# 删除
r = session.delete(f"{BASE_URL}/user/{USERNAME}", timeout=20)
print("DELETE:", r.status_code, r.text)
assert r.status_code == 200
# 再次查询
r = session.get(f"{BASE_URL}/user/{USERNAME}", timeout=20)
print("GET:", r.status_code, r.text)
assert r.status_code == 404

session.close()
print("DONE")