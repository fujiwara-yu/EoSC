from flask import Flask, render_template, request, redirect, url_for
from github import Github
import yaml
import collect
import json
from datetime import datetime
from pull_request_feature import get_pull_request_feature, get_pull_request_feature_list
import lib.pullrequest
import randomforest
import predict

def add_label(repo, number):
    f = open("settings.yaml", "r")
    settings = yaml.load(f, Loader=yaml.SafeLoader)

    token = settings["token"]
    client = Github(token, per_page=100)
    repo = client.get_repo(repo)
    pull = repo.get_pull(number)

    # ラベル名(判定結果から分類した結果のラベルを使うようにする)
    label = "Test"
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
    if hook["action"] == "reopened":
        # リポジトリ名とPR番号を引数に
        pr = lib.pullrequest.PullRequest(id, github_number, name, creator_name, None, created_at, None, None, None, commits, additions, deletions, changed_files, branch)
        pull_request_feature = get_pull_request_feature(pr)

        # TODO: 判定結果の扱い
        # hanteiから何をreturnするか
        # 判定結果をサーバに渡す or ラベルをつける
        predict.predict(pull_request_feature)
        add_label(repo, github_number)
    elif hook["action"] == "closed":
        # TODO: 保存機能
        # DB store
        # "commits" "additions" "deletions" "changed_files"
        # store
        list = get_pull_request_feature_list()
        randomforest.randomforest(list)
    #debug
    else:
        print(hook["action"])

    return request.get_data()

# TODO: サーバのPR一覧の表示について
@app.route('/')
def index():
    title = "ようこそ"
    #result = hantei.hantei("predict_bunkatsu.csv")
    head = result.columns
    body = result.values.tolist()
    # index.html をレンダリングする
    return render_template('index.html', head=head, body=body, title=title)

# /post にアクセスしたときの処理
@app.route('/post', methods=['GET', 'POST'])
def post():
    title = "こんにちは"
    if request.method == 'POST':
        # リクエストフォームから「名前」を取得して
        name = request.form['name']
        # index.html をレンダリングする
        return render_template('index.html', name=name, title=title)
    else:
        # エラーなどでリダイレクトしたい場合はこんな感じで
        return redirect(url_for('index'))

def start():
    app.debug = True
    app.run()

if __name__ == "__main__":
    start()