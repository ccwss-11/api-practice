"""
第 1 步：发一个最简单的 GET 请求。

运行：
    python 01_get.py

你要看懂：
- requests.get()
- r.status_code
- r.headers
- r.text
- r.json()
"""

import requests

URL = "https://petstore.swagger.io/v2/store/inventory"

# timeout=20 表示最多等 20 秒，防止请求卡死
r = requests.get(URL, timeout=20)

print("状态码:", r.status_code)
print("Content-Type:", r.headers.get("Content-Type"))
print("响应文本前 200 个字符:")
print(r.text[:200])

# r.json() 把 JSON 响应转成 Python 字典
data = r.json()
print("Python 类型:", type(data))
print("前 3 个库存:", list(data.items())[:3])
