# 11.18–11.19 接口实战：requests + pytest

> 被测 API：Swagger Petstore  
> Base URL：`https://petstore.swagger.io/v2`  
> 目标：
> - 11.18：用 Python requests 完成“创建用户 → 登录 → 查询 → 删除 → 再查 404”
> - 11.19：把 5 条手工接口用例转成 pytest

---

## 1. 项目结构

```text
api-practice/
├── conftest.py
├── pytest.ini
├── requirements.txt
├── requests_flow.py       # 11.18 独立 requests 脚本
├── tutorial/              # 零基础 4 步教程
│   ├── 01_get.py
│   ├── 02_get_params.py
│   ├── 03_post_json.py
│   └── 04_session_flow.py
├── tests/
│   └── test_user_api.py   # 11.19 pytest 用例
└── README.md
```

---

## 2. 怎么运行

### 11.18 先跑独立脚本

```powershell
cd D:\develop\qa-projects\api-practice
D:\develop\venvs\qa\Scripts\python.exe requests_flow.py
```

预期看到：

```text
CREATE: 200 ...
LOGIN: 200 ...
GET: 200 ...
DELETE: 200 ...
GET_AFTER_DELETE: 404 ...
DONE
```

### 11.19 再跑 pytest

```powershell
D:\develop\venvs\qa\Scripts\python.exe -m pytest -q
```

预期：

```text
5 passed
```

> 如果网络访问 Petstore 失败，先确认能打开：
> `https://petstore.swagger.io/v2/store/inventory`

---

## 3. 11.18 的 requests 链路

先看 `conftest.py` 里的 fixture：

- `base_url`：`https://petstore.swagger.io/v2`
- `username`：每次生成唯一用户名，避免数据冲突
- `user_payload`：创建用户的 JSON
- `session`：`requests.Session()`，复用 headers/连接
- `created_user`：创建用户，并在测试结束后清理

核心代码思路：

```python
r = session.post(f"{base_url}/user", json=user_payload, timeout=20)
r = session.get(f"{base_url}/user/login", params={"username": ..., "password": ...}, timeout=20)
r = session.get(f"{base_url}/user/{username}", timeout=20)
r = session.delete(f"{base_url}/user/{username}", timeout=20)
r = session.get(f"{base_url}/user/{username}", timeout=20)  # 404
```

重点：

- `json=` 发 JSON body
- `params=` 发 Query 参数
- `timeout=20` 防止卡死
- `r.status_code` 看 HTTP 状态码
- `r.json()` 取 JSON
- 每次创建唯一用户名，测试后清理

---

## 4. 11.19 的 5 条手工用例

| 手工用例 | pytest 函数 | 断言 |
|---|---|---|
| 创建用户成功 | `test_create_user` | 200；code=200；GET 能查到 |
| 正确密码登录 | `test_login_user` | 200；message 含 `logged in user session` |
| 查询用户 | `test_query_user` | 200；username/email 一致 |
| 删除用户 | `test_delete_user` | 200；再查 404 |
| 查询已删除用户 | `test_query_deleted_user_returns_404` | 404；message=User not found |

---

## 5. 为什么这么拆

- **一条测试函数只验证一个主要目的**。
- 公共数据准备放在 `conftest.py` 的 fixture 里，不重复写。
- 创建类测试必须清理数据，避免污染公共 API。
- 断言不只看状态码，还看关键字段。

---

## 6. 常见错误

1. **直接访问 `/v2` 看到 404**  
   `/v2` 是 base path，不是接口；要访问 `/v2/user/...`。

2. **用户名重复**  
   Petstore 会覆盖/冲突；用时间戳生成唯一用户名。

3. **不写 timeout**  
   公共 API 可能慢，测试会卡住。

4. **只看状态码**  
   200 也可能业务失败；要看 `code`/`message`/字段。

5. **不清理数据**  
   创建了 user 要 DELETE。

6. **fixture 作用域太大**  
   每个测试要独立用户时用 `function` scope，不要 `session`。

---

## 7. 下一步

先跑通 `5 passed`，然后把其中一条改成参数化：

```python
@pytest.mark.parametrize("password", ["Passw0rd!", "wrong"])
def test_login_password(...):
    ...
```

再往后，把 `requests` 换成 `requests.Session` + 封装的 `UserClient`，就是接口框架的雏形。
