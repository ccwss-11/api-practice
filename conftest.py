import time
import pytest
import requests

BASE_URL = "https://petstore.swagger.io/v2"


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL


@pytest.fixture
def username():
    # 每次生成唯一用户名，避免数据冲突
    return f"qa_{int(time.time() * 1000)}"


@pytest.fixture
def user_payload(username):
    return {
        "id": 0,
        "username": username,
        "firstName": "QA",
        "lastName": "Test",
        "email": "qa@example.com",
        "password": "Passw0rd!",
        "phone": "13800000000",
        "userStatus": 1,
    }


@pytest.fixture
def session():
    s = requests.Session()
    s.headers.update({"Accept": "application/json"})
    yield s
    s.close()


@pytest.fixture
def created_user(session, base_url, user_payload):
    r = session.post(f"{base_url}/user", json=user_payload, timeout=20)
    assert r.status_code == 200, r.text
    yield user_payload
    # 清理：不管测试有没有删，都尝试删一次
    session.delete(f"{base_url}/user/{user_payload['username']}", timeout=20)
