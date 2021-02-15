from os import replace
import numpy as np
from numpy.core.multiarray import result_type
import pandas as pd
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
import joblib
from sklearn.metrics import classification_report
import sys

# 引数でプロジェクト名指定
if len(sys.argv) != 2:
    print("No argument len")
    sys.exit()

project = sys.argv[1]

file_name = f"scripts/data/{project}_full.csv"
df_data = pd.read_csv(file_name)

file_name = f"scripts/data/pull_request_feature_{project}.csv"
df_new_feature = pd.read_csv(file_name)
df_new_feature = df_new_feature[["pr_branch_active", "pr_file_active", "github_number"]]


data = pd.merge(df_data, df_new_feature, left_on='github_id', right_on='github_number').drop(columns="github_number")

data.to_csv(f"{project}.csv")

print(data)