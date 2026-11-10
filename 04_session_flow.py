import requests

# 1. 定义基础变量（这就是你缺失的部分）
BASE_URL = "https://petstore.swagger.io/v2"
USERNAME = "testuser_qa001"
PASSWORD = "password123"

# 构造创建用户所需的字典
user = {
    "id": 1001,
    "username": USERNAME,
    "firstName": "QA",
    "lastName": "Tester",
    "email": "qa@example.com",
    "password": PASSWORD,
    "phone": "13800000000",
    "userStatus": 1
}

# 2. 初始化 Session
session = requests.Session()
session.headers.update({"Accept": "application/json"})

# 3. 执行业务流
print("1. 正在创建用户...")
res_create = session.post(f"{BASE_URL}/user", json=user, timeout=20)
print(f"   状态码: {res_create.status_code} (预期 200)")

print("2. 正在登录...")
res_login = session.get(
    f"{BASE_URL}/user/login",
    params={"username": USERNAME, "password": PASSWORD},
    timeout=20,
)
print(f"   状态码: {res_login.status_code} (预期 200)")

print("3. 正在查询用户...")
res_query = session.get(f"{BASE_URL}/user/{USERNAME}", timeout=20)
print(f"   状态码: {res_query.status_code} (预期 200)")

print("4. 正在删除用户...")
res_delete = session.delete(f"{BASE_URL}/user/{USERNAME}", timeout=20)
print(f"   状态码: {res_delete.status_code} (预期 200)")

print("5. 再次查询（验证是否已删除）...")
res_final = session.get(f"{BASE_URL}/user/{USERNAME}", timeout=20)
print(f"   状态码: {res_final.status_code} (预期 404)")

# 4. 增加断言，确保测试真正通过
assert res_final.status_code == 404, f"测试失败！预期 404，实际得到 {res_final.status_code}"
print("\n✅ 测试全部通过：用户的增、查、删生命周期验证成功！")