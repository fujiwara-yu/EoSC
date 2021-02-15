import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import sys

# 引数でプロジェクト名指定
if len(sys.argv) != 3:
    print("No argument len")
    sys.exit()

project = sys.argv[1]

max_num = int(sys.argv[2])

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

total_eval_u = 0
num_total = 0
loop_count = 1000
for i in range(loop_count):
    print("-------------------loop:",i+1, "-------------------")
    df_train = df_first_look.sample(frac=0.9).sort_index()
    num_train_data = df_train.shape[0]

    df_drop_train = df_first_look.drop(df_train.index).sort_index()
    df_predict = df_drop_train.sample(frac=1).sort_index()
    num_predict_data = df_predict.shape[0]

    num_predict_data = df_predict.shape[0]

    print(df_train.shape, df_predict.shape)

    # 必要なデータ取り出し
    train_data = df_train[["num_commits_open","lines_modified_open","files_modified_open","commits_on_files_touched","branch_hotness"]]
    train_label = df_train["useful"]
    predict_data = df_predict[["num_commits_open","lines_modified_open","files_modified_open","commits_on_files_touched","branch_hotness"]]
    predict_label = df_predict["useful"]

    clf = RandomForestClassifier(n_estimators=num_predict_data, max_depth=1000, max_features=3)
    clf.fit(train_data, train_label)

    result_predict = clf.predict(predict_data)
    result_predict_proba = clf.predict_proba(predict_data)

    predict_data_proba_label = df_predict[['useful']]
    predict_data_proba_label['result_predict_proba'] = result_predict_proba[:, 0]

    predict_data['predict_proba'] = result_predict_proba[:, 0]

    print(classification_report(predict_label, result_predict))

    predict_data['label'] = df_predict['useful']

    pre = predict_data.sort_values("predict_proba", ascending=False)

    num_data_u = len(pre)
    #print(use_datetime)
    #print(num_data_u)

    useful_limit = 100

    total_useful = 0
    precision = 0
    for i in range(num_data_u):
        if pre['label'][i] == 'useful':
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

with open(f'scripts/evaluation_ap/result/{project}_result.txt', 'w') as f:
    f.write(f"series: {total_eval_u/loop_count}\n")
    f.write(f"{num_total/loop_count}")
