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

print(a)
not_use_datetime = a["hyouka_1"]
use_datetime = a["hyouka_2"]
date = a.index.values
useful = a["label"]

not_use_datetime = not_use_datetime.rolling(5).mean()
use_datetime = use_datetime.rolling(5).mean()

print(not_use_datetime)

count = 0
i = 0
x = 0
ans_n = [0] * len(not_use_datetime)
ans_u = [0] * len(not_use_datetime)
for item in use_datetime:
    i += 1
    if not np.isnan(item):
        x += item
        ans_u[i-1] = x / i

i = 0
x = 0
for item in not_use_datetime:
    i += 1
    if not np.isnan(item):
        x += item
        ans_n[i-1] = x / i

sub = np.array(ans_n) - np.array(ans_u)
sub = np.abs(sub)
print(sub)

bitem = 0.0
for i, item in enumerate(sub):
    if item < 0.1 and bitem > 0.1:
        print(i)
        print(a.iloc[i][:])
    bitem = item

#ans_n = pd.DataFrame(ans_n).rolling(10).mean()
#ans_u = pd.DataFrame(ans_u).rolling(10).mean()

plt.title(f'時系列を考慮する場合としない場合の正解率の推移({project})')
plt.ylim(-0.05, 1.05)
plt.plot(date, ans_n, marker="o", label="時系列の考慮なし")
plt.plot(date, ans_u, marker="x", linestyle="dashed", label="時系列の考慮あり")
#plt.plot(date, sub, label="差分")
#plt.plot(date, [0.1] * len(date))
plt.legend()

# y軸のラベル
plt.xlabel("提案作成日時")
plt.xticks(rotation=45)

plt.ylabel("提案作成日時までの正解率")

# plt.grid(which='major',color='black',linestyle='--')

# 表示する
plt.show()

#plt.scatter(date, not_use_datetime, s=60, c="gray", alpha=0.5, linewidths="2",
#            edgecolors="black")
#plt.show()
#
#plt.scatter(date, use_datetime, s=60, c="gray", alpha=0.5, linewidths="2",
#            edgecolors="black")
#plt.show()
#