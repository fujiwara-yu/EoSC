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
file_name = f"scripts/data/{project}_new_f.csv"
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
# default
#train_data = df_train[["num_commits_open","lines_modified_open","files_modified_open","commits_on_files_touched","branch_hotness"]]
train_data = df_train[["lines_modified_open","commits_on_files_touched","branch_hotness"]]
train_label = df_train["useful"]

#predict_data = df_predict[["num_commits_open","lines_modified_open","files_modified_open","commits_on_files_touched","branch_hotness"]]
predict_data = df_predict[["lines_modified_open","commits_on_files_touched","branch_hotness"]]
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
#fi_sum =[0.0, 0.0, 0.0, 0.0, 0.0]
fi_sum =[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
total_eval0 = 0
total_eval1 = 0
total_eval2 = 0
df_accuracy = [0] * num_predict_data
pre = []
td = pd.DataFrame()
tl = pd.Series()

res = [0] * num_predict_data

with open(f'scripts/evaluation_old_feature_3f/result/{project}_result_f_new.txt', 'w') as f:
    f.write('num_train_data: ')
    f.write(str(num_train_data))

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

    predict_data['predict_proba'] = result_predict_proba[:, 0]

    print(classification_report(predict_label, result_predict))

    # Feature Importance
    fi = clf.feature_importances_

    print('Feature Importances:')
    print(fi)

    with open(f'scripts/evaluation_old_feature_3f/result/{project}_result_f_new.txt', 'w') as f:
        f.write('feature importance1\n')
        for i, feat in enumerate(train_data.columns):
            print('\t{0:20s} : {1:>.6f}'.format(feat, fi[i]))
            f.write('{0:20s} : {1:>.6f}\n'.format(feat, fi[i]))

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
            #train_data2 = row[["num_commits_open","lines_modified_open","files_modified_open","commits_on_files_touched","branch_hotness"]]
            #train_data2 = row[["branch_hotness","commits_on_files_touched", "pr_branch_active", "pr_file_active"]]
            train_data2 = row[["lines_modified_open","commits_on_files_touched","branch_hotness"]]

            train_data2 = pd.DataFrame([train_data2])
            train_label2 = row[["useful"]]
            i += 1
            continue
        elif i > 1:
            train_data2 = predict_data2
            train_label2 = predict_label2

        #predict_data2 = row[["num_commits_open","lines_modified_open","files_modified_open","commits_on_files_touched","branch_hotness"]]
        #predict_data2 = row[["branch_hotness","commits_on_files_touched", "pr_branch_active", "pr_file_active"]]
        predict_data2 = row[["lines_modified_open","commits_on_files_touched","branch_hotness"]]

        predict_data2 = pd.DataFrame([predict_data2])
        predict_label2 = row[["useful"]]

        # 一見か見る
        #first_look = df_first_look[["num_commits_open","lines_modified_open","files_modified_open","commits_on_files_touched","branch_hotness"]]
        #first_look = df_first_look[["branch_hotness","commits_on_files_touched", "pr_branch_active", "pr_file_active"]]
        first_look = df_first_look[["lines_modified_open","commits_on_files_touched","branch_hotness"]]

        first_look = pd.DataFrame(first_look)
        if first_look.shape[0] != j and train_data2.iloc[0].equals(first_look.iloc[j]):
            print("-------------------")
            print(train_data2)
            print(train_label2)
            print("-------------------")
            td = pd.concat([td, train_data2])
            tl = pd.concat([tl, train_label2])
            clf.fit(td, tl)
            j += 1


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
        pre_proba_tmp[i] = result_predict_proba[:, 0].sum()
        # pre_probaを使う
        pre_proba_sum2[i] = result_predict_proba[:, 0].sum()
        i += 1

        # Feature Importance
        fi = clf.feature_importances_

        print('Feature Importances:')
        fi_sum = [x + y for (x, y) in zip(fi, fi_sum)]
        for feat_i, feat in enumerate(train_data.columns):
            print('\t{0:20s} : {1:>.6f}'.format(feat, fi[feat_i]))

    fi_ave = [x / (i-1) for x in fi_sum]

    with open(f'scripts/evaluation_old_feature_3f/result/{project}_result_f_new.txt', 'a') as f:
        f.write('feature importance2\n')
        for feat_i, feat in enumerate(train_data.columns):
            print('\t{0:20s} : {1:>.6f}'.format(feat, fi_ave[feat_i]))
            f.write('{0:20s} : {1:>.6f}\n'.format(feat, fi_ave[feat_i]))



# それぞれのデータの正解した回数の平均
ave_list = [n/loop_count for n in useful_match]
ave_list2 = [n/loop_count for n in useful_match2]

#ave_list3 = [n/loop_count for n in pre_proba_sum]
#ave_list4 = [n/loop_count for n in pre_proba_sum2]


df['predict_proba'] = pre_proba_tmp


print("-----正解率-----")
print(ave_list)
print(ave_list2)
print("---------------")


with open(f'scripts/evaluation_old_feature_3f/result/{project}_result_f_new.txt', 'a') as f:
    f.write("-----正解率-----\n")
    f.write(', '.join(map(str, ave_list)))
    f.write('\n')
    f.write(', '.join(map(str, ave_list2)))
    f.write('\n')
    f.write("---------------\n")

predict_data['hyouka_1'] = np.array(ave_list)
#predict_data['hyouka_2'] = np.array(ave_list2)
df['hyouka_2'] = np.array(ave_list2)
#predict_data['hyouka_3'] = np.array(ave_list3)
#predict_data['hyouka_4'] = np.array(ave_list4)
predict_data['label'] = df_predict['useful']

print(predict_data)


joblib.dump(predict_data, f'scripts/evaluation_old_feature_3f/result/pull_request_feature_{project}.pkl')
joblib.dump(df, f'scripts/evaluation_old_feature_3f/result/pull_request_feature_series_{project}.pkl')
