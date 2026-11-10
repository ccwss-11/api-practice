import pytest


def test_create_user(session, base_url, user_payload):
    """手工用例 1：创建用户成功。"""
    r = session.post(f"{base_url}/user", json=user_payload, timeout=20)

    try:
        assert r.status_code == 200, r.text
        body = r.json()
        assert body["code"] == 200
        assert "message" in body

        # 查询确认真的创建成功
        r2 = session.get(f"{base_url}/user/{user_payload['username']}", timeout=20)
        assert r2.status_code == 200, r2.text
        user = r2.json()
        assert user["username"] == user_payload["username"]
        assert user["email"] == user_payload["email"]
    finally:
        session.delete(f"{base_url}/user/{user_payload['username']}", timeout=20)


def test_login_user(session, base_url, created_user):
    """手工用例 2：正确用户名 + 密码登录成功。"""
    r = session.get(
        f"{base_url}/user/login",
        params={
            "username": created_user["username"],
            "password": created_user["password"],
        },
        timeout=20,
    )

    assert r.status_code == 200, r.text
    body = r.json()
    assert body["code"] == 200
    assert "logged in user session" in body["message"]


def test_query_user(session, base_url, created_user):
    """手工用例 3：查询用户，字段与创建时一致。"""
    r = session.get(f"{base_url}/user/{created_user['username']}", timeout=20)

    assert r.status_code == 200, r.text
    user = r.json()
    assert user["username"] == created_user["username"]
    assert user["firstName"] == created_user["firstName"]
    assert user["lastName"] == created_user["lastName"]
    assert user["email"] == created_user["email"]


def test_delete_user(session, base_url, created_user):
    """手工用例 4：删除用户成功，再查返回 404。"""
    username = created_user["username"]

    r = session.delete(f"{base_url}/user/{username}", timeout=20)
    assert r.status_code == 200, r.text

    r2 = session.get(f"{base_url}/user/{username}", timeout=20)
    assert r2.status_code == 404, r2.text
    assert r2.json()["message"] == "User not found"


def test_query_deleted_user_returns_404(session, base_url, created_user):
    """手工用例 5：查询已删除用户，返回 404。"""
    username = created_user["username"]

    r = session.delete(f"{base_url}/user/{username}", timeout=20)
    assert r.status_code == 200, r.text

    r2 = session.get(f"{base_url}/user/{username}", timeout=20)
    assert r2.status_code == 404, r2.text
