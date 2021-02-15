import numpy as np
from numpy.core.multiarray import datetime_as_string
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

a = joblib.load(f"scripts/result/pull_request_feature_{project}.pkl")
b = joblib.load(f"scripts/result/pull_request_feature_series_{project}.pkl")
print(a)
print(b)
not_use_datetime = a["hyouka_1"]
use_datetime = b["hyouka_2"]

num_data_n = len(not_use_datetime)
num_data_u = len(use_datetime)

date_n = not_use_datetime.index.values
date_u = use_datetime.index.values

ans_n = [0] * num_data_n
ans_u = [0] * num_data_u
x = 0
for j in range(num_data_u):
    x += use_datetime.iloc[j]
    ans_u[j] = x / (j+1)

x = 0
for j in range(num_data_n):
    x += not_use_datetime.iloc[j]
    ans_n[j] = x / (j+1)

date_n = pd.DataFrame(date_n)
date_u = pd.DataFrame(date_u)
ans_n = pd.DataFrame(ans_n)
ans_u = pd.DataFrame(ans_u)

ans_n["datetime"] = date_n
ans_u["datetime"] = date_u

ans_n.set_index("datetime",inplace=True)
ans_u.set_index("datetime",inplace=True)
ans_n = ans_n.resample('M', label='left').mean().ffill()
ans_u = ans_u.resample('M', label='left').mean().ffill()
date_n = ans_n.index.values
date_u = ans_u.index.values

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

print(ans_n)
print(date_n)

sxmin='2010-08-01'
sxmax='2016-10-31'
xmin = datetime.datetime.strptime(sxmin, '%Y-%m-%d')
xmax = datetime.datetime.strptime(sxmax, '%Y-%m-%d')
plt.xlim(xmin, xmax)
plt.ylim(-0.05, 1.05)

plt.plot(date_n, ans_n, marker="o", label="時系列を考慮しなかった場合")
plt.plot(date_u, ans_u, marker="x", linestyle="dashed", label="時系列を考慮した場合")
plt.xticks(fontsize=16)
plt.yticks(fontsize=16)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=6))
plt.gca().xaxis.set_minor_locator(mdates.MonthLocator(interval=1))
plt.gca().tick_params(width = 2, length = 10)
plt.legend(fontsize=20)

# y軸のラベル
plt.xticks(rotation=90)
plt.ylabel("正解率", fontsize=16)

plt.grid(which='major',color='black',linestyle='--')

# 表示する
plt.show()
