from os import replace
import numpy as np
import pandas as pd
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
import joblib
from sklearn.metrics import classification_report
import sys
from sklearn.metrics import confusion_matrix
from sklearn.tree import export_graphviz
from sklearn import datasets
from sklearn import __version__ as sklearn_version
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn import tree
import pydotplus as pdp

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
#df_drop_train = df.drop(df_train.index).sort_index()
df_predict = df.drop(df_train.index).sort_index()

#df_predict = df_drop_train.sample(frac=1).sort_index()
num_predict_data = df_predict.shape[0]

num_predict_data = df_predict.shape[0]

print(df_train.shape, df_predict.shape)

# 必要なデータ取り出し
train_data = df_train[["num_commits_open","lines_modified_open","files_modified_open","commits_on_files_touched","branch_hotness"]]
train_label = df_train["useful"]
predict_data = df_predict[["num_commits_open","lines_modified_open","files_modified_open","commits_on_files_touched","branch_hotness"]]
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
total_eval0 = 0
total_eval1 = 0
total_eval2 = 0
df_accuracy = [0] * num_predict_data
pre = []

res = [0] * num_predict_data

with open(f'scripts/result/{project}_result.txt', 'w') as f:
    f.write('num_train_data: ')
    f.write(str(num_train_data))

# 評価のループ数
loop_count = 100
for i in range(loop_count):
    print("-------------------loop:",i+1, "-------------------")

    # 評価１
    # 時系列を考慮しない
    print("-----評価1-----")

    clf = RandomForestClassifier(n_estimators=num_predict_data, max_depth=1000, max_features=3)
    clf.fit(train_data, train_label)

    #clf = RandomForestClassifier(n_estimators=1, max_depth=1000, max_features=3, warm_start=True)
    #for index, row in df_train.iterrows():
    #    train_data = row[["num_commits_open","lines_modified_open","files_modified_open","commits_on_files_touched","branch_hotness"]]
    #    train_data = pd.DataFrame([train_data])
    #    train_label = row[["useful"]]
    #    clf.n_estimators = clf.n_estimators + 1
    #    clf.fit(train_data, train_label)

    result_predict = clf.predict(predict_data)
    result_predict_proba = clf.predict_proba(predict_data)

    print(result_predict_proba.tolist())

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
    #predict_data['predict_proba'] = result_predict_proba[:, 0]

    accuracy = metrics.accuracy_score(predict_label, result_predict)
    print("Accuracy:", accuracy)

    #                     Predicted
    #                 Negative  Positive
    #Actual Negative     TN        FP
    #       Positive     FN        TP
    #print(confusion_matrix(predict_label, result_predict, labels=['useless', 'useful']))

    #print(classification_report(predict_label, result_predict))

    #estimator = clf.estimators_[3]
    #dot_data = tree.export_graphviz(
    #                    estimator,
    #                    class_names=["useful", "useless"],
    #                    feature_names=["num_commits_open","lines_modified_open","files_modified_open","commits_on_files_touched","branch_hotness"],
    #                    filled=True,
    #                    rounded=True,
    #                    out_file=None
    #                )
    #graph = pdp.graph_from_dot_data(dot_data)
    #graph.write_png("bootstrap_tree.png")



# それぞれのデータの正解した回数の平均
ave_list = [n/loop_count for n in useful_match]


predict_data['hyouka_1'] = np.array(ave_list)
predict_data['label'] = df_predict['useful']

print(predict_data)

joblib.dump(predict_data, f'scripts/result/{project}.pkl')
