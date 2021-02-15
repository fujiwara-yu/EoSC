import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import joblib
import sys
import matplotlib.dates as mdates
import datetime
from dateutil.relativedelta import relativedelta

# 引数でプロジェクト名指定
if len(sys.argv) != 2:
    print("No argument len")
    sys.exit()

project = sys.argv[1]

a = joblib.load(f"scripts/evaluation_accuracy/result/{project}.pkl")
b = joblib.load(f"scripts/evaluation_accuracy/result/{project}_2.pkl")
c = joblib.load(f"scripts/evaluation_accuracy/result/{project}_1month.pkl")
d = joblib.load(f"scripts/evaluation_accuracy/result/{project}_5month.pkl")
e = joblib.load(f"scripts/evaluation_accuracy/result/{project}_10month.pkl")
f = joblib.load(f"scripts/evaluation_accuracy/result/{project}_15month.pkl")


not_use_datetime = a["hyouka_1"]
use_datetime = b["hyouka_2"]
short = c["hyouka_2"]
short2 = d["hyouka_2"]
short3 = e["hyouka_2"]
short4 = f["hyouka_2"]

#not_use_datetime = pd.DataFrame(not_use_datetime).resample('M').mean()
#use_datetime = pd.DataFrame(use_datetime).resample('M').mean()

num_data_n = len(not_use_datetime)
num_data_u = len(use_datetime)

date_n = not_use_datetime.index.values
date_u = use_datetime.index.values
date_s = short.index.values
date_s2 = short2.index.values
date_s3 = short3.index.values
date_s4 = short4.index.values

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

ans_s2 = [0] * num_data_u
x = 0
for j in range(num_data_u):
    if j < window:
        x += short2.iloc[j]
        ans_s2[j] = x / (j+1)
    else:
        x -= short2.iloc[j-window]
        x += short2.iloc[j]
        ans_s2[j] = x / window

ans_s3 = [0] * num_data_u
x = 0
for j in range(num_data_u):
    if j < window:
        x += short3.iloc[j]
        ans_s3[j] = x / (j+1)
    else:
        x -= short3.iloc[j-window]
        x += short3.iloc[j]
        ans_s3[j] = x / window

ans_s4 = [0] * num_data_u
x = 0
for j in range(num_data_u):
    if j < window:
        x += short4.iloc[j]
        ans_s4[j] = x / (j+1)
    else:
        x -= short4.iloc[j-window]
        x += short4.iloc[j]
        ans_s4[j] = x / window





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
date_s2 = pd.DataFrame(date_s2)
date_s3 = pd.DataFrame(date_s3)
date_s4 = pd.DataFrame(date_s4)
ans_n = pd.DataFrame(ans_n)
ans_u = pd.DataFrame(ans_u)
ans_s = pd.DataFrame(ans_s)
ans_s2 = pd.DataFrame(ans_s2)
ans_s3 = pd.DataFrame(ans_s3)
ans_s4 = pd.DataFrame(ans_s4)
#sub = pd.DataFrame(sub)

ans_n["datetime"] = date_n
ans_u["datetime"] = date_u
ans_s["datetime"] = date_s
ans_s2["datetime"] = date_s2
ans_s3["datetime"] = date_s3
ans_s4["datetime"] = date_s4


ans_n.set_index("datetime",inplace=True)
ans_u.set_index("datetime",inplace=True)
ans_s.set_index("datetime",inplace=True)
ans_s2.set_index("datetime",inplace=True)
ans_s3.set_index("datetime",inplace=True)
ans_s4.set_index("datetime",inplace=True)
ans_n = ans_n.resample('M', label='left').mean().ffill()
ans_u = ans_u.resample('M', label='left').mean()
ans_s = ans_s.resample('M', label='left').mean()
ans_s2 = ans_s2.resample('M', label='left').mean()
ans_s3 = ans_s3.resample('M', label='left').mean()
ans_s4 = ans_s4.resample('M', label='left').mean()
date_n = ans_n.index.values
date_u = ans_u.index.values
date_s = ans_u.index.values
date_s2 = ans_u.index.values
date_s3 = ans_u.index.values
date_s4 = ans_u.index.values

#date_n.drop(index=[n for n in range(100)], inplace=True)
#date_u.drop(index=[n for n in range(100)], inplace=True)
#ans_n.drop(index=[n for n in range(100)], inplace=True)
#ans_u.drop(index=[n for n in range(100)], inplace=True)
#sub.drop(index=[n for n in range(10)], inplace=True)



if len(ans_n) < len(ans_u):
    date = ans_n.tail(1).index.date
    date = date + relativedelta(months=1)
    date = date[0].strftime("%Y-%m-%d")
    date = datetime.datetime.strptime(date, '%Y-%m-%d')
    val = ans_n.tail(1)[0][0]
    df_tmp = pd.Series([val], index=[date])
    ans_n = pd.concat([ans_n, df_tmp])
    pd.to_datetime(date)
    date = np.datetime64(date)
    date_n = np.append(date_n, date)


sxmin='2011-03-01'
sxmax='2016-10-31'
xmin = datetime.datetime.strptime(sxmin, '%Y-%m-%d')
xmax = datetime.datetime.strptime(sxmax, '%Y-%m-%d')
#plt.xlim(xmin, xmax)

#plt.title(f'時系列を考慮する場合としない場合の正解率の推移({project})')
plt.ylim(-0.05, 1.05)
plt.plot(date_n, ans_n, marker="o", label="時系列の考慮なし")
plt.plot(date_u, ans_u, marker="x", linestyle="dashed", label="時系列の考慮あり")
plt.plot(date_u, ans_s, marker="s", linestyle="dashdot", label=f"時系列の考慮あり(1ヵ月)")
plt.plot(date_u, ans_s2, marker="^", linestyle="dotted", label=f"時系列の考慮あり(5ヵ月)")
plt.plot(date_u, ans_s3, marker="D", linestyle="dashed", label=f"時系列の考慮あり(10ヵ月)")
plt.plot(date_u, ans_s4, marker="+", linestyle="dashdot", label=f"時系列の考慮あり(15ヵ月)")
#plt.plot(date, sub, label="正解率の差")
#plt.plot(date, [0.1] * len(date))

plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=6))
plt.gca().xaxis.set_minor_locator(mdates.MonthLocator(interval=1))
plt.gca().tick_params(width = 2, length = 10)

plt.legend(fontsize=20, ncol=2)
# y軸のラベル
#plt.xlabel("プロジェクト発足時からの経過月数")
#plt.xlabel("提案作成日時")
plt.xticks(rotation=90)
plt.ylabel("正解率", fontsize=16)
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