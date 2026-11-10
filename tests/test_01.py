import requests
import pytest
import datetime

BASE_URL = "https://petstore.swagger.io/v2"
UNIQUE_ID = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
USERNAME = f"test{UNIQUE_ID}"
PASSWORD = "password"


@pytest.fixture(scope="module")
def api_session():
    session = requests.Session()
    session.headers.update({"accept": "application/json"})
    yield session # 把session交给测试用例使用
    session.close()
@pytest.fixture(scope="module")
def user_data():
    return {
        "id": UNIQUE_ID,
        "username": USERNAME,
        "firstName": "QA",
        "lastName": "Test",
        "email": "qa@example.com",
        "password": PASSWORD,
        "phone": "13800000000",
        "userStatus": 1
    }
# 正常创建用户
def test_user_create_success(api_session, user_data):
    r = api_session.post(f"{BASE_URL}/user",json = user_data,timeout=20)
    assert r.status_code == 200
    assert r.json().get("code") == 200
# 登录
def test_user_login_success(api_session, user_data):
    r = api_session.get(
        f"{BASE_URL}/user/login",
        params = {"username": USERNAME, "password": PASSWORD},
        timeout=20)
    assert r.status_code == 200
    assert "logged in user session" in r.json()["message"]
# 查询
def test_user_check_success(api_session, user_data):
    r = api_session.get(f"{BASE_URL}/user/{USERNAME}")
    assert r.status_code == 200
    assert r.json()["username"] == USERNAME
    assert r.json()["email"] == user_data["email"]
# 删除
def test_user_delete_success(api_session, user_data):
    r = api_session.delete(f"{BASE_URL}/user/{USERNAME}")
    assert r.status_code == 200
# 再次查询
def test_user_select_all_success(api_session, user_data):
    r = api_session.get(f"{BASE_URL}/user/{USERNAME}")
    assert r.status_code == 404
# 密码错误
def test_wrong_password(api_session ):
    r = api_session.get(
        f"{BASE_URL}/user/login",
        params = {"username": USERNAME, "password": "1234567"},
        timeout=20
                        )

    assert "Invalid username or password" in r.json()["message"] or r.status_code == 400




