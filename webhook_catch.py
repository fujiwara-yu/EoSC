from flask import Flask, request
from github import Github
import sys
import yaml
import collect
import json

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

@app.route("/pr_event", methods=['POST'])
def get_pr():
    print(request.headers)
    hook = json.loads(request.get_data())

    # actionで分岐
    # open => 判定 + ラベルづけ
    # closed => DBに保存
    if hook["action"] == "opened":
        # リポジトリ名とPR番号を引数に
        add_label(hook["pull_request"]["head"]["repo"]["full_name"], hook["number"])
    elif hook["action"] == "closed":
        # DB store
        pass
    #debug
    else:
        print(hook["action"])

    return request.get_data()


if __name__ == "__main__":
    app.debug = True
    app.run()
