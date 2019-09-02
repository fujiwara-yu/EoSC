import pandas as pd
from sklearn import svm, metrics
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
import sys

def hantei(file):
    # 予測モデルを復元
    clf = joblib.load('model.pkl')

    #予測データの読み込み
    test_csv = pd.read_csv(file)
    test_data = test_csv[["num_commits_open","lines_modified_open","files_modified_open","commits_on_files_touched","branch_hotness"]]
    test_label = test_csv["useful"]

    # 予測結果を出力
    pre = clf.predict(test_data)
    p = clf.predict_proba(test_data)[:,0]
    ac_score = metrics.accuracy_score(test_label, pre)
    #print("テストラベル=", test_label)
    print("解析結果=", pre)
    print("解析結果=", p)
    print("正解率=", ac_score)

    result_csv = pd.DataFrame(columns=['name','created_at','predict', 'url'])
    result_csv['name'] = test_csv['title']
    result_csv['created_at'] = test_csv['created_at']
    result_csv['predict'] = p
    result_csv['predict'] = result_csv['predict'].round(3)
    result_csv['url'] = test_csv['url']
    return result_csv

if __name__=="__main__":
    args = sys.argv
    # 引数ないとき
    if(len(args) != 2):
        print("Not argument")
        sys.exit()
    wariai = hantei(args[1])
    print(wariai)