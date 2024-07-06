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
Cardi = 100 # カーディナリティ制約
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
code_ = []
for i in range(Cardi):
    code_.append(lst_sort[i][2]) # 上位10銘柄の銘柄コードをcode_に格納

# Jquantsから株価データを取得
import requests
import json
# import pandas as pd
mail_password={"mailaddress":"e.cos2612@outlook.jp", "password":"26Erika12122"}
r_ref = requests.post("https://api.jquants.com/v1/token/auth_user", data=json.dumps(mail_password))
RefreshToken = r_ref.json()["refreshToken"]
r_token = requests.post(f"https://api.jquants.com/v1/token/auth_refresh?refreshtoken={RefreshToken}")
idToken = r_token.json()["idToken"]
headers = {'Authorization': 'Bearer {}'.format(idToken)}

# 2023年度の構成銘柄上位10個の株価データ取得
Close_Values = [[] for _ in range(Cardi)]
time_point = []
from_ = "2023-04-01"
to_ = "2024-03-31"

for i in range(Cardi):
    res = requests.get(f"https://api.jquants.com/v1/prices/daily_quotes?code={code_[i]}&from={from_}&to={to_}", headers=headers)
    data = res.json()
    close_values = [quote["Close"] for quote in data["daily_quotes"]]
    for j in range(len(close_values)):
        if i==0:
            time_point.append(data["daily_quotes"][j]["Date"])
        Close_Values[i].append(close_values[j])
        
# print(Close_Values[i][0])
# print("銘柄コード", code_, "の", data["daily_quotes"][100]["Date"], "の株価:", data["daily_quotes"][100]["Close"])
# print(data["daily_quotes"][100]["Date"])

# TOPIXの値動き取得
import pandas_datareader.data as web
from datetime import date
import pandas as pd
point_topix = []

source = 'stooq'
dt_s = date(2023, 4, 1)
dt_e = date(2024, 3, 29)
symbol = '^TPX'
df_topix = web.DataReader(symbol, source, dt_s, dt_e)
df_topix = df_topix.sort_values("Date").reset_index()
# print(df_topix.at[0, "Close"]) # pandasでデータ取得するときはatとか使う
for i in range(len(df_topix)):
    point_topix.append(df_topix.at[i, "Close"])




# 4. グラフ化
import matplotlib.pyplot as plt
import japanize_matplotlib
from matplotlib.ticker import MaxNLocator
japanize_matplotlib.japanize()

price_buy = close_values[0]
point_portfolio = []
for i in range(Cardi):
    for j in range(len(Close_Values[i])):
        if i==0:
            point_portfolio.append(Close_Values[i][j] - Close_Values[i][0])
        else:
            point_portfolio[j] = point_portfolio[j] + Close_Values[i][j] - Close_Values[i][0]


fig, ax1 = plt.subplots()
# TOPIXのプロット
ax1.plot(time_point, point_topix, label='TOPIX', color='blue')
ax1.set_ylabel('TOPIX', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')
ax1.xaxis.set_major_locator(MaxNLocator(nbins=5))
plt.xticks(rotation=30)

# Portfolioのプロット
ax2 = ax1.twinx()
ax2.plot(time_point, point_portfolio, label='Portfolio', color='green')
ax2.set_ylabel('ポートフォリオ', color='green')
ax2.tick_params(axis='y', labelcolor='green')

# グラフの表示
plt.title("2023年度のTOPIXとポートフォリオ,  C={}".format(Cardi))
fig.tight_layout()
plt.show()

