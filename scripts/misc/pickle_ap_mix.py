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

b = joblib.load(f"scripts/result/{project}_2.pkl")
b = DataFrame(b)

##########################
# コアユーザの抽出

# bのuserから一見ユーザを取り出す
df_first_look = b.copy()
df_first_look.drop_duplicates(subset='requester', inplace=True)
df_core = b.drop(df_first_look.index).sort_index()

df_first_look = df_first_look[["predict_proba", "useful"]]
df_core = df_core[["predict_proba", "useful"]]
###########################

total_eval_u = 0
max_num = 48
num_total = 0
loop_count = 1000
for i in range(loop_count):
    df_first_look_train = df_first_look.sample(frac=0.9)
    df_predict = df.drop(df_train.index).sort_index()

    use_datetime = pd.merge(df_core, df_first_look_test, how="outer")
    use_datetime = use_datetime.sort_values("predict_proba", ascending=False)

    num_data_u = len(use_datetime)
    #print(use_datetime)
    print(num_data_u)

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
