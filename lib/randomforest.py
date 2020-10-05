import sys
import os

app_home = os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)) , ".." ))
sys.path.append(os.path.join(app_home))
sys.path.append(os.path.join(app_home,"lib"))

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.externals import joblib
import sys

def randomforest(pull_request_feature_list):

    train_data = pd.DataFrame(columns=["num_commits_open","lines_modified_open","files_modified_open","commits_on_files_touched","branch_hotness"])
    train_label = pd.DataFrame(columns=["useful"])

    for prf in pull_request_feature_list:
        tmp_se = pd.Series( [prf.commits, prf.fix_len, prf.changed_files, prf.file_active, prf.branch_active], index=train_data.columns )
        train_data = train_data.append(tmp_se, ignore_index=True)
        tmp_se = pd.Series( [prf.useful], index=train_label.columns )
        train_label = train_label.append(tmp_se, ignore_index=True)

    train_label = train_label['useful']

    clf = RandomForestClassifier(n_estimators = 1000, max_depth = 10, max_features = 5)
    clf.fit(train_data, train_label)

    joblib.dump(clf, app_home + '/db/model.pkl')
    print("create model")
