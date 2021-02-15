from os import replace
import numpy as np
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
df_train = df_first_look.sample(frac=0.9).sort_index()
num_train_data = df_train.shape[0]

# テストデータをサンプリング
# コアユーザ含めている
df_drop_train = df.drop(df_train.index).sort_index()

df_predict = df_drop_train.sample(frac=1).sort_index()
num_predict_data = df_predict.shape[0]

#df_predict_drop = df_drop_train.sample(n=500).sort_index()
#Jdf_predict = df_predict_drop.resample('M').ffill()
#df_predict = df_drop_train.resample('W').ffill()
#df_predict.set_index('created_at', inplace=True)
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

    clf = RandomForestClassifier(n_estimators = 1000, max_features = 5, random_state=0)
    clf.fit(train_data, train_label)

    # probaがどっちに分類されるかの確率を出しているのでこっち使う
    # [[有益確率, 無益確率] ... ] 有益確率だけあれば良い
    result_predict = clf.predict(predict_data)
    result_predict_proba = clf.predict_proba(predict_data)

    # usefulの確率だけ取り出し
    # print(result_predict_proba[:, 0])

    accuracy = metrics.accuracy_score(predict_label, result_predict)
    print("Accuracy:", accuracy)

    precision = metrics.precision_score(predict_label, result_predict, average=None)
    print("Precision:", precision)

    recall = metrics.recall_score(predict_label, result_predict, average=None)
    print("Recall:", recall)

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
    #print("new:", predict_data)

    # ランダム(ただの時系列順)
    predict_data_proba_label.sample(frac=1, replace=True)
    # print(predict_data_proba_label)

    total_useful_rand = 0
    precision_rand = 0
    for i in range(num_predict_data):
        if predict_data_proba_label['useful'][i] == 'useful':
            total_useful_rand = total_useful_rand + 1
            precision_rand = precision_rand + total_useful_rand / (i+1)

    total_eval0 = total_eval0 +  precision_rand / total_useful_rand
    print("ap_rand:", total_eval0)

    # 結果で並べ替え
    pre_sort = predict_data_proba_label.sort_values('result_predict_proba', ascending=False)
    # print(pre_sort)

    # 並べ替えた結果から平均適合率だす
    total_useful = 0
    precision = 0
    for i in range(num_predict_data):
        if pre_sort['useful'][i] == 'useful':
            total_useful = total_useful + 1
            precision = precision + total_useful / (i+1)

    total_eval1 = total_eval1 + precision / total_useful
    print("ap_not_time series:", total_eval1)

    print(classification_report(predict_label, result_predict))

    ####################################
    # ここから評価値を時系列データごとに算出 #
    ####################################

    # result_predictとpredict_labelの比較をすればいい
    #data = pd.DataFrame(predict_label)
    #data['result'] = result_predict

    #x = 0
    #y = 0
    #l = []
    #for i in range(num_predict_data):
    #    for j in range(i+1):
    #        #print(data.iloc[j]['useful'])
    #        if data.iloc[j]['result'] == "useful":
    #            x += 1
    #            if data.iloc[j]['useful'] == "useful":
    #                y += 1

    #    if x == 0:
    #        x = 1

    #    l.append(y / x)

    #res += np.array(l)
    #print(res)

    # 評価２
    # 時系列を考慮
    print("-----評価2-----")
    i = 0
    previous_index = pd.Timestamp(2000, 1, 1, 1)
    clf = RandomForestClassifier(n_estimators=1, max_features=5, warm_start=True)
    for index, row in df.iterrows():
        print("predict:",i)
        #train = df_train.query('@previous_index < index and index < @index')
        #train = df_train.query('@previous_index < index and index < @index')
        #print(train)
        #with open(f'scripts/result/{project}_result.txt', 'a') as f:
        #    f.write(str(i+1))
        #    f.write(', ')
        #    f.write(str(train.shape[0]))
        #    f.write('\n')


        #train_data2 = train[["num_commits_open","lines_modified_open","files_modified_open","commits_on_files_touched","branch_hotness"]]
        #train_label2 = train["useful"]
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

        #if len(train["useful"].unique()) == 2 or i == 0:
        if train_data2.shape[0] != 0:
            previous_index = index
            clf.n_estimators = clf.n_estimators + 1
            print("-------------------")
            print(train_data2)
            print(train_label2)
            print("-------------------")

            clf.fit(train_data2, train_label2)

        result_predict = clf.predict(predict_data2)
        # probaがどっちに分類されるかの確率を出しているのでこっち使う
        # [[有益確率, 無益確率] ... ] 有益確率だけあれば良い
        result_predict_proba = clf.predict_proba(predict_data2)

        # usefulの確率だけ取り出し
        #print(result_predict_proba[:, 0])
        #print("predict=", result_predict)

        result = (result_predict == predict_label2.values)
        if result:
            useful_match2[i] = useful_match2[i] + 1

        pre.append(result_predict)

        # pre_probaを使う
        pre_proba_sum2[i] = result_predict_proba[:, 0].sum()
        # print("pre_proba_sum2:", pre_proba_sum2)
        i += 1

    #total_predict_proba = np.array(total_predict_proba) + np.array(pre_proba_sum2)
    #predict_data_proba_label['eval2'] = np.array(pre_proba_sum2)

    #print("sum:",predict_data_proba_label)

    ## 結果で並べ替え
    #pre_sort2 = predict_data_proba_label.sort_values('eval2', ascending=False)
    #total_useful = 0
    #precision = 0
    #for i in range(num_predict_data):
    #    if pre_sort2['useful'][i] == 'useful':
    #        total_useful = total_useful + 1
    #        precision = precision + total_useful / (i+1)

    #total_eval2 = total_eval2 + precision / total_useful
    #print("eval2:", total_eval2)


# それぞれのデータの正解した回数の平均
ave_list = [n/loop_count for n in useful_match]
ave_list2 = [n/loop_count for n in useful_match2]

ave_list3 = [n/loop_count for n in pre_proba_sum]
ave_list4 = [n/loop_count for n in pre_proba_sum2]

#precision_list = res / loop_count
#precision_list2 = total_predict_proba / loop_count
random = total_eval0 / loop_count
sort_no_time_series = total_eval1 / loop_count
sort_time_series = total_eval2 / loop_count



print("-----正解率-----")
print(ave_list)
print(ave_list2)
print("---------------")

#print("-----適合率-----")
#print(precision_list)
#print(precision_list2)
#print("----------------")

# 何回かやった結果の平均を求める
print("-----平均適合率-----")
print("random:", random)
print("sort_no_time_series:", sort_no_time_series)
print("sort_time_series:", sort_time_series)
print("------------------")

with open(f'scripts/result/{project}_result.txt', 'a') as f:
    f.write("-----正解率-----\n")
    f.write(', '.join(map(str, ave_list)))
    f.write('\n')
    f.write(', '.join(map(str, ave_list2)))
    f.write('\n')
    f.write("---------------\n")
    #f.write("-----適合率-----\n")
    #f.write(', '.join(map(str, precision_list)))
    #f.write('\n')
    #f.write(', '.join(map(str,precision_list2)))
    #f.write('\n')
    #f.write("----------------\n")
    f.write("-----平均適合率-----\n")
    f.write(str(random))
    f.write('\n')
    f.write(str(sort_no_time_series))
    f.write('\n')
    f.write(str(sort_time_series))
    f.write('\n')
    f.write("------------------\n")



# 使わなさそうな気がするからコメントアウト
#print(ave_list3)
#print(ave_list4)

predict_data['hyouka_1'] = np.array(ave_list)
#predict_data['hyouka_2'] = np.array(ave_list2)
df['hyouka_2'] = np.array(ave_list2)
#predict_data['hyouka_3'] = np.array(ave_list3)
#predict_data['hyouka_4'] = np.array(ave_list4)
predict_data['label'] = df_predict['useful']

print(predict_data)

joblib.dump(df, f'scripts/result/{project}_2.pkl')
joblib.dump(predict_data, f'scripts/result/{project}.pkl')
