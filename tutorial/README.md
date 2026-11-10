# Python requests 入门：4 个脚本，一步一步来

> 不要一上来写完整链路。按 01 → 02 → 03 → 04 顺序跑。

## 准备工作

```powershell
cd D:\develop\qa-projects\api-practice
D:\develop\venvs\qa\Scripts\python.exe --version
```

确认能看到 Python 3.15。

---

## 01_get.py：最简单的 GET

```powershell
D:\develop\venvs\qa\Scripts\python.exe tutorial\01_get.py
```

学：

- `requests.get(url, timeout=20)`
- `r.status_code`
- `r.headers`
- `r.text`
- `r.json()`

看到 `状态码: 200` 就对了。

---

## 02_get_params.py：带 Query 参数

```powershell
D:\develop\venvs\qa\Scripts\python.exe tutorial\02_get_params.py
```

学：

- `params={"status": "available"}` 会自动拼成 `?status=available`
- `r.url` 看最终地址
- `len(r.json())` 看数组长度

---

## 03_post_json.py：POST JSON + 查询 + 删除

```powershell
D:\develop\venvs\qa\Scripts\python.exe tutorial\03_post_json.py
```

学：

- `requests.post(..., json=user)` 自动设置 `Content-Type: application/json`
- 创建后 `GET` 查询，确认数据真的存在
- 最后 `DELETE` 清理

---

## 04_session_flow.py：Session 串完整链路

```powershell
D:\develop\venvs\qa\Scripts\python.exe tutorial\04_session_flow.py
```

学：

- `requests.Session()` 复用 headers/连接
- 创建 → 登录 → 查询 → 删除 → 再查 404
- `assert` 检查状态码

看到 `DONE` 就对了。

---

## 改代码练习

1. 把 03 的 `email` 改成你的邮箱，看 GET 返回是否变化。
2. 把 04 的登录密码改成 `wrong`，看哪一行 assert 失败。
3. 把 02 的 `status` 改成 `sold`，看返回数量变化。
4. 在 04 里加一条 `print(r.headers)`，看响应头。

---

## 常见错误

| 错误 | 原因 |
|---|---|
| `ModuleNotFoundError: requests` | 没用 QA 虚拟环境 |
| 404 | URL 少了 `/v2` 或路径写错 |
| 401/403 | 缺 token/api_key |
| 请求卡住 | 没写 `timeout` |
| `JSONDecodeError` | 响应不是 JSON，先 `print(r.text)` |
