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
RefreshToken = r_ref.json()["refreshToken"]
r_token = requests.post(f"https://api.jquants.com/v1/token/auth_refresh?refreshtoken={RefreshToken}")
idToken = r_token.json()["idToken"]
headers = {'Authorization': 'Bearer {}'.format(idToken)}

code_ = "7203"
from_ = "2023-04-01"
to_ = "2024-03-31"

res = requests.get(f"https://api.jquants.com/v1/prices/daily_quotes?code={code_}&from={from_}&to={to_}", headers=headers)
data = res.json()
# print(data)
# print("銘柄コード", code_, "の", data["daily_quotes"][100]["Date"], "の株価:", data["daily_quotes"][100]["Close"])
close_values = [quote["Close"] for quote in data["daily_quotes"]]
# print(close_values[1])
# print(data["daily_quotes"][100]["Date"])



# 4. グラフ化
import matplotlib.pyplot as plt
import japanize_matplotlib
from matplotlib.ticker import MaxNLocator
japanize_matplotlib.japanize()

price_buy = close_values[0]
graph_point = []
time_point = []
for x in range(len(close_values)):
    graph_point.append(close_values[x] - price_buy)
    time_point.append(data["daily_quotes"][x]["Date"])
# print(len(close_values))

# plt.plot(time_point, graph_point)
fig, ax = plt.subplots()
ax.plot(time_point, graph_point)
ax.xaxis.set_major_locator(MaxNLocator(nbins=5))

plt.xticks(rotation=30)
plt.title("2023年4月から2024年3月までの基準価格推移")  
plt.ylabel("基準価格")
plt.show()





# for x in range(0, 12):
#     graph_point[x] = total_net_assets[x] / total_unit