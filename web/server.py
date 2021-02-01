import sys
import os

app_home = os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)) , ".." ))
sys.path.append(os.path.join(app_home))
sys.path.append(os.path.join(app_home,"lib"))

from lib.pullrequestfeature import PullRequestFeatureController
from flask import Flask, render_template, request
from github import Github
import yaml
import lib.collect
import json
from datetime import datetime
import lib.pullrequest
import lib.randomforest
import lib.predict
import csv

# yamlファイルの読み込み
f = open(app_home + "/settings.yaml", "r")
settings = yaml.load(f, Loader=yaml.SafeLoader)

user = settings["user"]
repo = settings["repo"]

# TODO: ラベルをつける条件
# 上位のいくつかにラベルをつける
# 現在ラベルがついているものよりも有益な提案と予測されたものはラベルをつける
# ラベルの数が一定以下になったら既存の提案にラベルをつける
def add_label(repo, number):
    f = open("settings.yaml", "r")
    settings = yaml.load(f, Loader=yaml.SafeLoader)

    token = settings["token"]
    client = Github(token, per_page=100)
    repo = client.get_repo(repo)
    pull = repo.get_pull(number)

    # ラベル名(判定結果から分類した結果のラベルを使うようにする)
    label = "Priority"
    pull.add_to_labels(label)

app = Flask(__name__)

# GitHubのイベントを監視して，条件により処理
# 1. PRがopenedされたらDBに追加する処理
# 2. PRがclosedされたら有益度合いを判定し，ラベルをつける処理
@app.route("/pr_event", methods=['POST'])
def pr_event():
    print(request.headers)
    hook = json.loads(request.get_data())

    # actionで分岐
    # open => 判定 + ラベルづけ
    # closed => DBに保存
    repo = hook["pull_request"]["head"]["repo"]["full_name"]
    id = hook["pull_request"]["id"]
    github_number = hook["number"]
    name = hook["pull_request"]["title"]
    creator_name = hook["pull_request"]["user"]["login"]
    created_at = datetime.strptime(hook["pull_request"]["created_at"], '%Y-%m-%dT%H:%M:%SZ')
    changed_files = hook["pull_request"]["changed_files"]
    commits = hook["pull_request"]["commits"]
    additions = hook["pull_request"]["additions"]
    deletions = hook["pull_request"]["deletions"]
    branch = hook["pull_request"]["base"]["repo"]["default_branch"]
    if hook["action"] == "opened":
        # リポジトリ名とPR番号を引数に
        pr = lib.pullrequest.PullRequest(id, github_number, name, creator_name, None, created_at, None, None, None, commits, additions, deletions, changed_files, branch)
        pull_request_feature = PullRequestFeatureController.get_pull_request_feature(pr)

        # webサービスの更新
        pre_proba = lib.predict.predict(pull_request_feature)
        lib.predict.data_store(pr, pre_proba)

        # ラベル貼り付け
        add_label(repo, github_number)
        print("pull request is predicted")

    elif hook["action"] == "closed":
        # Delete file
        lib.predict.data_drop()
        # DB store
        lib.collect.run(github_number)

        # TODO: CSVから読み込む
        # learn
        pull_request_feature_list = []
        with open(app_home + '/db/pull_request_feature.csv', 'r') as f:
            reader = csv.reader(f)
            l = [row for row in reader]
            pull_request_feature_list.append(l[1:])

        pull_request_feature = PullRequestFeatureController.get_pull_request_feature()
        pull_request_feature_list.append(pull_request_feature)
        lib.randomforest.randomforest(pull_request_feature_list)

    #debug
    else:
        print(hook["action"])

    return request.get_data()

@app.route('/home')
def index():
    title = "有益提案抽出支援システム"

    result = []
    with open(app_home + '/db/used_num.txt', 'r') as f:
        used_num = [s.strip() for s in f.readlines()]

    tmp = {}
    for data_num in used_num:
        with open(app_home + f'/db/data/data{data_num}.json', 'r') as f:
            tmp = json.load(f)

        tmp['created_at'] = datetime.strptime(tmp['created_at'], '%Y-%m-%dT%H:%M:%S')
        tmp.update(url=f"https://github.com/{user}/{repo}/pull/{tmp['github_number']}")
        result.append(tmp)


    # index.html をレンダリングする
    return render_template('index.html', project=f"{user}/{repo}", body=result, title=title)

@app.route('/home', methods=['POST'])
def search():
    title = "有益提案抽出支援システム"
    pr_name = request.form['pr_name']
    print(request.form['start'])
    if request.form['start']:
        start = datetime.strptime(request.form['start'] , '%Y-%m-%d')
    else:
        start = datetime.strptime("2000-01-01", '%Y-%m-%d')
    if request.form['end']:
        end = datetime.strptime(request.form['end'] , '%Y-%m-%d')
    else:
        end = datetime.strptime("3000-01-01", '%Y-%m-%d')

    result = []
    with open(app_home + '/db/used_num.txt', 'r') as f:
        used_num = [s.strip() for s in f.readlines()]

    tmp = {}
    for data_num in used_num:
        with open(app_home + f'/db/data/data{data_num}.json', 'r') as f:
            tmp = json.load(f)

        if pr_name in tmp['name']:
            tmp['created_at'] = datetime.strptime(tmp['created_at'], '%Y-%m-%dT%H:%M:%S')
            if tmp['created_at'] > start and tmp['created_at'] < end:
                tmp.update(url=f"https://github.com/{user}/{repo}/pull/{tmp['github_number']}")
                result.append(tmp)

    # index.html をレンダリングする
    return render_template('index.html', project=f"{user}/{repo}", body=result, title=title)

def start():
    app.debug = True
    app.run()

if __name__ == "__main__":
    start()