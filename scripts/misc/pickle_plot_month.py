import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import joblib
import sys

# 引数でプロジェクト名指定
if len(sys.argv) != 3:
    print("No argument len")
    sys.exit()

project = sys.argv[1]
month = sys.argv[2]

a = joblib.load(f"scripts/result/{project}.pkl")
b = joblib.load(f"scripts/result/{project}_2.pkl")
c = joblib.load(f"scripts/result/{project}_{month}month.pkl")


not_use_datetime = a["hyouka_1"]
use_datetime = b["hyouka_2"]
short = c["hyouka_2"]

#not_use_datetime = pd.DataFrame(not_use_datetime).resample('M').mean()
#use_datetime = pd.DataFrame(use_datetime).resample('M').mean()

num_data_n = len(not_use_datetime)
num_data_u = len(use_datetime)

date_n = not_use_datetime.index.values
date_u = use_datetime.index.values
date_s = short.index.values

#plt.title(f'時系列を考慮する場合としない場合の正解率の推移({project})')
#plt.ylim(-0.05, 1.05)
#plt.plot(date_n, not_use_datetime, marker="o", label="時系列の考慮なし")
#plt.plot(date_u, use_datetime, marker="x", linestyle="dashed", label="時系列の考慮あり")
#plt.legend()
#plt.xlabel("提案作成日時")
#plt.ylabel("提案作成時点からの予測結果の正解率")
#plt.grid(which='major',color='black',linestyle='--')
#plt.show()
#exit()

window = 50000
count = 0
ans_n = [0] * num_data_n
ans_u = [0] * num_data_u
x = 0
for j in range(num_data_u):
    if j < window:
        x += use_datetime.iloc[j]
        ans_u[j] = x / (j+1)
    else:
        x -= use_datetime.iloc[j-window]
        x += use_datetime.iloc[j]
        ans_u[j] = x / window

x = 0
for j in range(num_data_n):
    if j < window:
        x += not_use_datetime.iloc[j]
        ans_n[j] = x / (j+1)
    else:
        x -= not_use_datetime.iloc[j-window]
        x += not_use_datetime.iloc[j]
        ans_n[j] = x / window


ans_s = [0] * num_data_u
x = 0
for j in range(num_data_u):
    if j < window:
        x += short.iloc[j]
        ans_s[j] = x / (j+1)
    else:
        x -= short.iloc[j-window]
        x += short.iloc[j]
        ans_s[j] = x / window





#sub = np.array(ans_n) - np.array(ans_u)
#sub = np.abs(sub)
#print(sub)

#bitem = 0.0
#for i, item in enumerate(sub):
#    if item < 0.1 and bitem > 0.1:
#        print(i)
#        print(a.iloc[i][:])
#    bitem = item

#ans_n = pd.DataFrame(ans_n).rolling(3).mean()
#ans_u = pd.DataFrame(ans_u).rolling(3).mean()
#sub = pd.DataFrame(sub).rolling(3).mean()

date_n = pd.DataFrame(date_n)
date_u = pd.DataFrame(date_u)
date_s = pd.DataFrame(date_s)
ans_n = pd.DataFrame(ans_n)
ans_u = pd.DataFrame(ans_u)
ans_s = pd.DataFrame(ans_s)
#sub = pd.DataFrame(sub)

ans_n["datetime"] = date_n
ans_u["datetime"] = date_u
ans_s["datetime"] = date_s


ans_n.set_index("datetime",inplace=True)
ans_u.set_index("datetime",inplace=True)
ans_s.set_index("datetime",inplace=True)
ans_n = ans_n.resample('M').mean()
ans_u = ans_u.resample('M').mean()
ans_s = ans_s.resample('M').mean()
date_n = ans_n.index.values
date_u = ans_u.index.values
date_s = ans_u.index.values

#date_n.drop(index=[n for n in range(100)], inplace=True)
#date_u.drop(index=[n for n in range(100)], inplace=True)
#ans_n.drop(index=[n for n in range(100)], inplace=True)
#ans_u.drop(index=[n for n in range(100)], inplace=True)
#sub.drop(index=[n for n in range(10)], inplace=True)

plt.title(f'時系列を考慮する場合としない場合の正解率の推移({project})')
plt.ylim(-0.05, 1.05)
plt.plot(date_n, ans_n, marker="o", label="時系列の考慮なし")
plt.plot(date_u, ans_u, marker="x", linestyle="dashed", label="時系列の考慮あり")
plt.plot(date_u, ans_s, marker="x", linestyle="dashed", label=f"時系列の考慮あり({month}ヶ月)")
#plt.plot(date, sub, label="正解率の差")
#plt.plot(date, [0.1] * len(date))

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=3))
plt.gca().xaxis.set_minor_locator(mdates.MonthLocator(interval=1))

plt.legend()

# y軸のラベル
#plt.xlabel("プロジェクト発足時からの経過月数")
plt.xlabel("提案作成日時")
plt.xticks(rotation=90)
plt.ylabel("提案作成時点からの予測結果の正解率")

plt.grid(which='major',color='black',linestyle='--')

# 表示する
plt.show()
#
#plt.scatter(np.array(date_n), np.array(not_use_datetime), s=60, c="gray", alpha=0.5, linewidths="2",
#            edgecolors="black")
#plt.show()
#
#plt.scatter(np.array(date_u), np.array(use_datetime), s=60, c="gray", alpha=0.5, linewidths="2",
#            edgecolors="black")
#plt.show()
#