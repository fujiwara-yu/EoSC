import pandas as pd
from sklearn import svm, metrics
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
import sys
#from sklearn.model_selection import cross_val_score
def randomforest(file):
    ## ファイル読み込み
    csv = pd.read_csv(file)
    csv_data = csv[["num_commits_open","lines_modified_open","files_modified_open","commits_on_files_touched","branch_hotness"]]
    csv_label = csv["useful"]

    train_data = csv_data
    train_label = csv_label
    #test_csv = pd.read_csv(file)
    #test_data = test_csv[["num_commits_open","lines_modified_open","files_modified_open","commits_on_files_touched","branch_hotness"]]
    #test_data = [[1,52,9,19.0412491,152.1414052]]
    #test_label = test_csv["useful"]
    clf = RandomForestClassifier(n_estimators = 1000, max_depth = 10, max_features = 5)
    clf.fit(train_data, train_label)
    #pre = clf.predict(test_data)
    #ac_score = metrics.accuracy_score(test_label, pre)
    #print("テストラベル=", test_label)
    #print("解析結果=", pre)
    #print("正解率=", ac_score)

    joblib.dump(clf, 'model.pkl')
    print("create model")

if __name__=="__main__":
    args = sys.argv
    # 引数ないとき
    if(len(args) != 2):
        print("Not argument")
        sys.exit()

    randomforest(args[1])
