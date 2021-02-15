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

a = joblib.load(f"scripts/result/{project}.pkl")
b = joblib.load(f"scripts/result/{project}_2.pkl")
c = joblib.load(f"scripts/result/{project}.pkl")
d = joblib.load(f"scripts/result/{project}_2.pkl")
#print(a)
#print(b)
not_use_datetime = a[["predict_proba", "label"]].sort_values("predict_proba", ascending=False)
use_datetime = b[["predict_proba", "useful"]].sort_values("predict_proba", ascending=False)

print(not_use_datetime)
print(use_datetime)

num_data_n = len(not_use_datetime)
num_data_u = len(use_datetime)

useful_limit = 100

# ランダム
total_eval_n = 0
loop_count = 0
for j in range(1000):
    rand = c[["predict_proba", "label"]].sample(frac=1)
    total_useful = 0
    precision = 0
    for i in range(num_data_n):
        if rand['label'][i] == 'useful':
            total_useful = total_useful + 1
            precision = precision + total_useful / (i+1)
            if total_useful == useful_limit:
                loop_count = j
                break

    loop_count = j
    total_eval_n = total_eval_n + precision / total_useful

print(f"rand1: {total_eval_n/loop_count}")

# ランダム
total_eval_n = 0
loop_count = 0
for j in range(1000):
    rand = d[["predict_proba", "useful"]].sample(frac=1)
    total_useful = 0
    precision = 0
    for i in range(num_data_n):
        if rand['useful'][i] == 'useful':
            total_useful = total_useful + 1
            precision = precision + total_useful / (i+1)
            if total_useful == useful_limit:
                loop_count = j
                break

    loop_count = j
    total_eval_n = total_eval_n + precision / total_useful

print(f"rand2: {total_eval_n/loop_count}")



total_useful = 0
precision = 0
for i in range(num_data_n):
    if not_use_datetime['label'][i] == 'useful':
        total_useful = total_useful + 1
        precision = precision + total_useful / (i+1)
        if total_useful == useful_limit:
            break

total_eval_n = precision / total_useful
print(f"not_series: {total_eval_n}")
print(total_useful)

total_useful = 0
precision = 0
for i in range(num_data_u):
    if use_datetime['useful'][i] == 'useful':
        total_useful = total_useful + 1
        precision = precision + total_useful / (i+1)
        if total_useful == useful_limit:
            break


total_eval_u = precision / total_useful
print(f"series: {total_eval_u}")
print(total_useful)

exit()

print("----------------No.3------------------")
total_eval_n_list = []
total_eval_u_list = []
for year in range(2011, 2017):
    for month in range(1, 13):
        prev = f'{year}-{month}'
        prev = f'{year}-{month}'
        not_month = not_use_datetime[prev]
        u_month = use_datetime[prev]
        nm_len = len(not_month)
        um_len = len(u_month)
        if nm_len > 1 and um_len > 1:
            print(prev)
            print(not_month)
            total_useful = 0
            precision = 0
            for i in range(nm_len):
                if not_month['label'][i] == 'useful':
                    total_useful = total_useful + 1
                    precision = precision + total_useful / (i+1)
                    if total_useful == useful_limit:
                        break

            total_eval_n = precision / total_useful
            print(f"not_series: {total_eval_n}")
            print(total_useful)
            total_eval_n_list.append(total_eval_n)

            total_useful = 0
            precision = 0
            for i in range(um_len):
                if u_month['useful'][i] == 'useful':
                    total_useful = total_useful + 1
                    precision = precision + total_useful / (i+1)
                    if total_useful == useful_limit:
                        break

            total_eval_u = precision / total_useful
            print(f"series: {total_eval_u}")
            print(total_useful)
            total_eval_u_list.append(total_eval_u)

print(total_eval_n_list)
print(total_eval_u_list)

print(np.average(total_eval_n_list))
print(np.average(total_eval_u_list))

exit()

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
