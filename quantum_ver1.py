# # 変数配列の作成
# from amplify import VariableGenerator
# gen = VariableGenerator()
# q = gen.array("Binary", 2)
# print(q)

# # 目的関数の作成
# f = q[0] * q[1] + q[0] -q[1] + 1
# print(f)

# from amplify import FixstarsClient
# client = FixstarsClient()
# client.token = "AE/VfQDHqAtq9NOTUnJyxWiDTSGa7avMJQe" 
# client.parameters.timeout = 1000
# from amplify import solve
# result = solve(f, client)

# print(result.best.values)
# print(result.best.objective)
# print(f"{q} = {q.evaluate(result.best.values)}")

# 1. 変数の初期設定等
from amplify import VariableGenerator
gen = VariableGenerator()
q = gen.array("Binary", 100)
C = 100 # カーディナリティ制約
# total_net_assets[0] = 1000000 # 純資産総額
total_unit = 1000000 # 総口数


# 2. TOPIX2146銘柄を取得
import csv
with open("topixweight_j.csv") as file:
    lst = list(csv.reader(file))

# データ以外の記述をリストから削除、0～2145までがデータ
lst.pop(0)
last_data = 2145
for i in range(18):
    lst.pop( last_data + 1 )


# 3. 銘柄、購入数の決定
lst_sort = sorted(lst, reverse=True, key=lambda x: x[4])
# for i in range(10):
#     print(lst_sort[i])

# Jquantsから株価データを取得
import requests
import json
import pandas as pd
mail_password={"mailaddress":"e.cos2612@outlook.jp", "password":"26Erika12122"}
r_ref = requests.post("https://api.jquants.com/v1/token/auth_user", data=json.dumps(mail_password))
# print(r_ref.json())
RefreshToken = r_ref.json()["refreshToken"]
r_token = requests.post(f"https://api.jquants.com/v1/token/auth_refresh?refreshtoken={RefreshToken}")
# print(r_token.json())

idToken = r_token.json()["idToken"]
headers = {'Authorization': 'Bearer {}'.format(idToken)}

code_ = "7203"
res = requests.get(f"https://api.jquants.com/v1/prices/daily_quotes?code={code_}&date=20230324", headers=headers)
data = res.json()
print("銘柄コード", code_, "の株価:", data["daily_quotes"][0]["Close"])


# for x in data:
#     print(x[Close])


# 4. グラフ化

# for x in range(0, 12):
#     graph_point[x] = total_net_assets[x] / total_unit