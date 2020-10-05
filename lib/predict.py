import sys
import os

app_home = os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)) , ".." ))
sys.path.append(os.path.join(app_home))
sys.path.append(os.path.join(app_home,"lib"))

from lib.pullrequestfeature import *
from lib.pullrequest import *
import pandas as pd
from sklearn.externals import joblib
import json
import yaml
from github import Github

# yamlファイルの読み込み
f = open(app_home + "/settings.yaml", "r")
settings = yaml.load(f, Loader=yaml.SafeLoader)
# tokenの設定
token = settings["token"]

# データを収集するリポジトリの設定
user = settings["user"]
repo = settings["repo"]
user_repo = user + "/" + repo

client = Github(token, per_page=100)
target_repo = client.get_repo(user_repo)

def predict(prf):
    # 予測モデルを復元
    clf = joblib.load(app_home + '/db/model.pkl')

    predict_data = pd.DataFrame(columns=["num_commits_open","lines_modified_open","files_modified_open","commits_on_files_touched","branch_hotness"])
    predict_label = pd.DataFrame(columns=["useful"])

    tmp_se = pd.Series( [prf.commits, prf.fix_len, prf.changed_files, prf.file_active, prf.branch_active], index=predict_data.columns )
    predict_data = predict_data.append(tmp_se, ignore_index=True)
    tmp_se = pd.Series( [prf.useful], index=predict_label.columns )
    predict_label = predict_label.append(tmp_se, ignore_index=True)

    predict_label = predict_label['useful']

    pre = clf.predict(predict_data)
    pre_proba = clf.predict_proba(predict_data)[:,0]

    print("解析結果=", pre)
    print("解析結果=", pre_proba)
    return pre_proba[0]

# jsonに保存
# 必要なデータ github_number, title, creator_name, created_at, pre_proba
def data_store(pr, pre_proba):
    if not os.path.exists(app_home + '/db/used_num.txt'):
        with open(app_home + '/db/used_num.txt', 'w') as f:
            f.write('')

    data_num = 0
    with open(app_home + '/db/used_num.txt', 'r') as f:
        used_num = [s.strip() for s in f.readlines()]

    print(used_num)

    for n in range(1000):
        if not str(n) in used_num:
            data_num = n
            print(data_num)
            break

    dic = {"github_number": pr.github_number, "name": pr.name, "creator_name": pr.creator_name, "created_at": pr.created_at.isoformat(), "pre_proba": pre_proba}
    with open(app_home + f'/db/data/data{data_num}.json', 'w') as f:
        json.dump(dic, f, indent=2, ensure_ascii=False)

    with open(app_home + '/db/used_num.txt', 'a') as f:
        f.write(str(data_num))
        f.write("\n")

def data_drop(data_num):
    os.remove(app_home + f'/db/data/data{data_num}.json')

    with open(app_home + '/db/used_num.txt', 'r') as f:
        used_num = [s.strip() for s in f.readlines()]

    used_num.remove(str(data_num))

    with open(app_home + '/db/used_num.txt', 'w') as f:
        f.write('\n'.join(used_num))
        f.write("\n")

# openの取り出して予測
def opened_all():
    pr_list = target_repo.get_pulls(state='opened', sort='created')
    for pr in pr_list:
        pr = PullRequest(pr.id, pr.number, pr.title, pr.user.login, pr.body, pr.created_at, pr.closed_at, pr.merged_at, pr.state, pr.commits, pr.additions, pr.deletions, pr.changed_files, pr.base.repo.default_branch)
        prf = PullRequestFeatureController.get_pull_request_feature(pr)

        pre_proba = predict(prf)
        data_store(pr, pre_proba)
