import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import joblib
import sys

# 引数でプロジェクト名指定
if len(sys.argv) != 2:
    print("No argument len")
    sys.exit()

project = sys.argv[1]


a = joblib.load(f"scripts/result/{project}.pkl")
b = joblib.load(f"scripts/result/{project}_2.pkl")

not_use_datetime = a["hyouka_1"]
use_datetime = b["hyouka_2"]

#not_use_datetime = pd.DataFrame(not_use_datetime).resample('M').mean()
#use_datetime = pd.DataFrame(use_datetime).resample('M').mean()

num_data_n = len(not_use_datetime)
num_data_u = len(use_datetime)

date_n = not_use_datetime.index.values
date_u = use_datetime.index.values

total_useful = 0
total_useful_t = 0
ans_n = [0] * num_data_n
for i in range(num_data_n):
    if a['label'][i] == 'useful' and a['hyouka_1'][i] == 1.0:
        total_useful += 1
        total_useful_t += 1
    elif a['label'][i] == 'useful' and a['hyouka_1'][i] == 0.0:
        total_useful += 1


    if total_useful == 0:
        ans_n[i] = 0
    else:
        ans_n[i] = total_useful_t / total_useful

total_useful = 0
total_useful_t = 0
ans_u = [0] * num_data_u
for i in range(num_data_u):
    if b['useful'][i] == 'useful' and b['hyouka_2'][i] == 1.0:
        total_useful += 1
        total_useful_t += 1
    elif b['useful'][i] == 'useful' and b['hyouka_2'][i] == 0.0:
        total_useful += 1

    if total_useful == 0:
        ans_u[i] = 0
    else:
        ans_u[i] = total_useful_t / total_useful



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
ans_n = pd.DataFrame(ans_n)
ans_u = pd.DataFrame(ans_u)
#sub = pd.DataFrame(sub)

#ans_n["datetime"] = date_n
#ans_u["datetime"] = date_u
#ans_n.set_index("datetime",inplace=True)
#ans_u.set_index("datetime",inplace=True)
#ans_n = ans_n.resample('M').mean()
#ans_u = ans_u.resample('M').mean()
#date_n = ans_n.index.values
#date_u = ans_u.index.values
#
#print(ans_n)

#date_n.drop(index=[n for n in range(100)], inplace=True)
#date_u.drop(index=[n for n in range(100)], inplace=True)
#ans_n.drop(index=[n for n in range(100)], inplace=True)
#ans_u.drop(index=[n for n in range(100)], inplace=True)
#sub.drop(index=[n for n in range(10)], inplace=True)

plt.title(f'時系列を考慮する場合としない場合の正解率の推移({project})')
plt.ylim(-0.05, 1.05)
plt.plot(date_n, ans_n, marker="o", label="時系列の考慮なし")
plt.plot(date_u, ans_u, marker="x", linestyle="dashed", label="時系列の考慮あり")
#plt.plot(date, sub, label="正解率の差")
#plt.plot(date, [0.1] * len(date))
plt.legend()

# y軸のラベル
#plt.xlabel("プロジェクト発足時からの経過月数")
plt.xlabel("提案作成日時")
#plt.xticks(rotation=45)
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