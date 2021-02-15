from os import replace
import numpy as np
from numpy.core.multiarray import datetime_as_string
import pandas as pd
import matplotlib.pyplot as plt
import joblib
import sys
import matplotlib.dates as mdates
import datetime
from dateutil.relativedelta import relativedelta
from pandas.core.frame import DataFrame

# 引数でプロジェクト名指定
if len(sys.argv) != 2:
    print("No argument len")
    sys.exit()

project = sys.argv[1]



b = joblib.load(f"scripts/evaluation_new_feature_3f/result/pull_request_feature_series_{project}.pkl")
b = DataFrame(b)

# bのuserから一見ユーザを取り出す
df_first_look = b.copy()
df_first_look.drop_duplicates(subset='requester', inplace=True)
#print(df_first_look.shape[0])
#print(df_first_look)

df_first_look = df_first_look[["predict_proba", "useful"]]

# 取り出せる最大個数
max_num =47

total_eval_u = 0
num_total = 0
loop_count = 1000
for i in range(loop_count):
    use_datetime = df_first_look.sample(frac=0.1)
    use_datetime = use_datetime.sort_values("predict_proba", ascending=False)

    num_data_u = len(use_datetime)

    useful_limit = 10000

    total_useful = 0
    precision = 0
    for i in range(num_data_u):
        if use_datetime['useful'][i] == 'useful':
            total_useful = total_useful + 1
            precision = precision + total_useful / (i+1)
            if total_useful == useful_limit:
                break
        if i == max_num:
            num = total_useful

    num_total = num_total + num
    total_eval_u = total_eval_u + precision / total_useful


print(f"series: {total_eval_u/loop_count}")
print(f"{num_total/loop_count}")
