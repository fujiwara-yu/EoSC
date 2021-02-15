from os import replace
import numpy as np
from numpy.core.multiarray import result_type
import pandas as pd
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
import joblib
from sklearn.metrics import classification_report
import sys
from dateutil.relativedelta import relativedelta
import datetime

# 引数でプロジェクト名指定
if len(sys.argv) != 3:
    print("No argument len")
    sys.exit()

project = sys.argv[1]
month = int(sys.argv[2])

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
td = pd.DataFrame()
tl = pd.Series()

res = [0] * num_predict_data

# 評価のループ数
loop_count = 1
for i in range(loop_count):
    print("-------------------loop:",i+1, "-------------------")

    # 評価１
    # 時系列を考慮しない
    print("-----評価1-----")

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

    # 評価２
    # 時系列を考慮
    print("-----評価2-----")
    i = 0
    j = 0
    previous_index = pd.Timestamp(2000, 1, 1, 1)
    clf = RandomForestClassifier(n_estimators=1000, max_depth=1000, max_features=3, random_state=0)
    for index, row in df.iterrows():
        print("predict:",i)

        if i == 0:
            train_data2 = row[["num_commits_open","lines_modified_open","files_modified_open","commits_on_files_touched","branch_hotness"]]
            train_data2 = pd.DataFrame([train_data2])
            train_label2 = row[["useful"]]
            i += 1
            continue
        elif i > 1:
            train_data2 = predict_data2
            train_label2 = predict_label2

        predict_data2 = row[["num_commits_open","lines_modified_open","files_modified_open","commits_on_files_touched","branch_hotness"]]
        predict_data2 = pd.DataFrame([predict_data2])
        predict_label2 = row[["useful"]]

        # 一見か見る
        first_look = df_first_look[["num_commits_open","lines_modified_open","files_modified_open","commits_on_files_touched","branch_hotness"]]
        first_look = pd.DataFrame(first_look)
        if first_look.shape[0] != j and train_data2.iloc[0].equals(first_look.iloc[j]):
            print("-------------------")
            print(train_data2)
            print(train_label2)
            # 学習データの月を見て，期間以前のは削除
            now_datetime = train_data2.index.date
            previous = now_datetime[0] - relativedelta(months=month)

            td = pd.concat([td, train_data2])
            tl = pd.concat([tl, train_label2])

            tdd = td[previous:]
            num_previous = td[:previous].shape[0]
            tld = tl[num_previous:]

            clf.fit(tdd, tld)
            j += 1

            print("num_train_data:", tdd.shape[0])
            print("-------------------")

            # Feature Importance
            fi = clf.feature_importances_

            print('Feature Importances:')
            for i, feat in enumerate(iris['feature_names']):
                print('\t{0:20s} : {1:>.6f}'.format(feat, fti[i]))


        result_predict = clf.predict(predict_data2)
        result_predict_proba = clf.predict_proba(predict_data2)

        #print("proba:", result_predict_proba)
        # usefulの確率だけ取り出し
        #print(result_predict_proba[:, 0])
        #print("predict=", result_predict)

        result = (result_predict == predict_label2.values)
        if result:
            useful_match2[i] = useful_match2[i] + 1

        pre.append(result_predict)

        # pre_probaを使う
        pre_proba_sum2[i] = result_predict_proba[:, 0].sum()
        i += 1



# それぞれのデータの正解した回数の平均
ave_list = [n/loop_count for n in useful_match]
ave_list2 = [n/loop_count for n in useful_match2]

#ave_list3 = [n/loop_count for n in pre_proba_sum]
#ave_list4 = [n/loop_count for n in pre_proba_sum2]




print("-----正解率-----")
print(ave_list)
print(ave_list2)
print("---------------")


predict_data['hyouka_1'] = np.array(ave_list)
#predict_data['hyouka_2'] = np.array(ave_list2)
df['hyouka_2'] = np.array(ave_list2)
#predict_data['hyouka_3'] = np.array(ave_list3)
#predict_data['hyouka_4'] = np.array(ave_list4)
predict_data['label'] = df_predict['useful']

print(predict_data)

joblib.dump(df, f'scripts/evaluation_accuracy/result/{project}_{month}month.pkl')
