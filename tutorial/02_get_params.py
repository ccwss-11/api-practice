"""
第 2 步：带 Query 参数的 GET。

运行：
    python 02_get_params.py

你要看懂：
- params 字典会自动拼成 ?status=available
- r.url 是最终请求地址
- len(r.json()) 看数组长度
"""

import requests

URL = "https://petstore.swagger.io/v2/pet/findByStatus"

params = {"status": "available"}

r = requests.get(URL, params=params, timeout=20)

print("最终 URL:", r.url)
print("状态码:", r.status_code)

pets = r.json()
print("返回数量:", len(pets))
print("第一条:", pets[0] if pets else "空数组")
