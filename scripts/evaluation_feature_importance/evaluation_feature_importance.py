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

## ファイル読み込み
file_name = f"scripts/data/{project}_full.csv"
df = pd.read_csv(file_name)
print("全データ数", df.shape[0])

###
### 読み込んだデータの前処理
###

# 作成日時をDateTime型に変換
df['created_at'] = pd.to_datetime(df['created_at'].astype(int), unit='s')

# datetime列をindexにする
df.set_index('created_at', inplace=True, drop=False)

# indexであるdatetimeのdtype='object' を dtype='datetime64[ns]' に変更
df.index = pd.to_datetime(df.index, format='%Y-%m-%d')

# PR作成日時順に並べ替え
df = df.sort_index()

# 一見ユーザのみ取り出す
df_first_look = df.copy()
df_first_look.drop_duplicates(subset='requester', inplace=True)
print(df_first_look.shape[0])
print(df_first_look)

# 学習データをサンプリング
# fracでデータから何割をランダムに取り出すか決める
# 一見ユーザの9割にしている
df_train = df_first_look.sample(frac=1).sort_index()
num_train_data = df_train.shape[0]

# テストデータをサンプリング
# コアユーザ含めている
df_drop_train = df.drop(df_train.index).sort_index()

df_predict = df_drop_train.sample(frac=1).sort_index()
num_predict_data = df_predict.shape[0]

num_predict_data = df_predict.shape[0]

print(df_train.shape, df_predict.shape)

# 必要なデータ取り出し
train_data = df_train[["num_commits_open","lines_modified_open","files_modified_open","commits_on_files_touched","branch_hotness"]]
#train_data = df_train[["lines_modified_open","commits_on_files_touched","branch_hotness"]]
train_label = df_train["useful"]
predict_data = df_predict[["num_commits_open","lines_modified_open","files_modified_open","commits_on_files_touched","branch_hotness"]]
#predict_data = df_predict[["lines_modified_open","commits_on_files_touched","branch_hotness"]]
predict_label = df_predict["useful"]

# 初期化
pre_sum = 0
pre_proba_sum = [0] * num_predict_data
pre_proba_sum2 = [0] * num_predict_data
pre_proba_sum2 = [0] * df.shape[0]
total_predict_proba = [0] * num_predict_data
total_predict_proba = [0] * df.shape[0]
useful_match = [0] * num_predict_data
useful_match2 = [0] * num_predict_data
useful_match2 = [0] * df.shape[0]
pre_proba_tmp = [0] * df.shape[0]
fi_sum =[0.0, 0.0, 0.0, 0.0, 0.0]
total_eval0 = 0
total_eval1 = 0
total_eval2 = 0
df_accuracy = [0] * num_predict_data
pre = []
td = pd.DataFrame()
tl = pd.Series()

res = [0] * num_predict_data

clf = RandomForestClassifier(n_estimators=num_predict_data, max_depth=1000, max_features=3, random_state=0)
clf.fit(train_data, train_label)

result_predict = clf.predict(predict_data)
result_predict_proba = clf.predict_proba(predict_data)

# 評価値算出 一致したものの割合 有益無益関係なし
result = (result_predict == predict_label.values)
for i in range(num_predict_data):
    if result[i]:
        useful_match[i] = useful_match[i] + 1

# pre_probaを使う
pre_proba_sum = pre_proba_sum + result_predict_proba[:, 0]
print("pre_proba_sum:", pre_proba_sum)

predict_data_proba_label = df_predict[['useful']]
predict_data_proba_label['result_predict_proba'] = result_predict_proba[:, 0]

predict_data['predict_proba'] = result_predict_proba[:, 0]

print(classification_report(predict_label, result_predict))

# Feature Importance
fi = clf.feature_importances_

print('Feature Importances:')
print(fi)

with open(f'scripts/evaluation_feature_importance/result/{project}_result_old_f5.txt', 'w') as f:
    f.write('feature importance1\n')
    for i, feat in enumerate(train_data.columns):
        print('\t{0:20s} : {1:>.6f}'.format(feat, fi[i]))
        f.write('{0:20s} : {1:>.6f}\n'.format(feat, fi[i]))
