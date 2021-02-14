#!/usr/bin/env python
import sys
import os

app_home = os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)) , ".." ))
sys.path.append(os.path.join(app_home))
sys.path.append(os.path.join(app_home,"lib"))

from github import Github
import time
import yaml
import lib.database
import datetime

# DB接続
db = lib.database.Database()
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


def rate_limit_controll():
    # APIの制限メッセージ
    rate_remaining = client.rate_limiting
    print(f"limit: {rate_remaining}")
    if (rate_remaining[0] < 10):
        print("API limit\nPlease wait 1 hour")
        print(datetime.datetime.now())
        time.sleep(3600)

#def rate_limit_controll():
#    # APIの制限メッセージ
#    rate_limit = client.get_rate_limit()
#    print(f"limit: {rate_limit.core}")
#    if (rate_limit.core.remaining < 10):
#        print("API limit\nPlease wait 1 hour")
#        time.sleep(3600)

# PRをDBに保存する
def get_pull_requests(pulls):
    print("Get pull_requests start")
    insert_pull_requests = "INSERT IGNORE INTO pull_requests (id, github_number, name, creator_name, body, created_at, closed_at, merged_at, state, commits, additions, deletions, changed_files, branch) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"

    for pr in pulls:
        insert_data = ()
        insert_data = (pr.id, pr.number, pr.title, pr.user.login, pr.body, pr.created_at, pr.closed_at, pr.merged_at, pr.state, pr.commits, pr.additions, pr.deletions, pr.changed_files, pr.base.repo.default_branch)
        print(insert_data)
        db.insert(insert_pull_requests, insert_data)
        rate_limit_controll()


    print("Get pull finish")

# PRとかのcommentをDBに保存
def get_pull_request_comments(issues):
    print("Get pull_request_comments start")
    insert_comments = "INSERT IGNORE INTO pull_request_comments (id, pull_request_id, creator_name, created_at, body) VALUES (%s, %s, %s, %s, %s);"
    for iss in issues:
        comments = iss.get_comments()
        rate_limit_controll()
        for prc in comments:
            insert_data = ()
            insert_data = (prc.id, iss.number, prc.user.login, prc.created_at, prc.body)
            print(insert_data)
            db.insert(insert_comments, insert_data)

    print("Get pull_comment finish")

def get_pull_commits(pulls):
    print("Get pull_commits start")
    insert_commits = "INSERT IGNORE INTO commits (sha, pull_request_id, creator_name, created_at, body, state) VALUES (%s, %s, %s, %s, %s, %s);"
    #pulls = repo.get_pulls(state='close', sort='created')
    state = "pull_request"
    for pull in pulls:
        print(pull.number)
        commits = pull.get_commits()
        for commit in commits:
            com = target_repo.get_commit(commit.sha)
            if com.author is not None:
                insert_data = ()
                insert_data = (com.sha, pull.id, com.author.login, com.commit.author.date, com.commit.message, state)
                print(insert_data)
                db.insert(insert_commits, insert_data)

                for file in com.files:
                    file_id = add_file(file.filename)
                    get_commits_files(com.sha, file_id)

            rate_limit_controll()

    print("Get pull_commit finish")

# 初期: その時点のproject commitの取得とPRとの関係性を保存
# 継続: project commitの追加とPRとの関係性の変更
def get_project_commits(pulls=None):
    print("Get project_commits start")

    insert_commits = "INSERT IGNORE INTO commits (sha, pull_request_id, creator_name, created_at, body, state) VALUES (%s, %s, %s, %s, %s, %s);"
    if pulls is None:
        commits = target_repo.get_commits()
    else:
        query = 'SELECT created_at FROM commits ORDER BY created_at DESC LIMIT 1'
        previous_created_at = db.select(query)[0][0] + datetime.timedelta(seconds=1)
        commits = target_repo.get_commits(since=previous_created_at)

    state = "project"
    for com in commits:
        if com.author is not None:
            insert_data = ()
            insert_data = (com.sha, None, com.author.login, com.commit.author.date, com.commit.message, state)
            print(insert_data)

            query = "UPDATE commits SET state=%s WHERE sha=%s"
            db.insert(query, ('pull_request_and_project', com.sha))
            db.insert(insert_commits, insert_data)

            for file in com.files:
                file_id = add_file(file.filename)
                get_commits_files(com.sha, file_id)
                rate_limit_controll()

    print("Get project_commit finish")


def get_commits_files(commit_sha, file_id):
    insert_commits_files = "INSERT IGNORE INTO commits_files (commit_sha, file_id) VALUES (%s, %s);"
    x = ()
    x = (commit_sha, file_id)
    print(x)
    db.insert(insert_commits_files, x)

def add_file(file):
    insert_files = "INSERT IGNORE INTO project_files (name) VALUES (%s);"
    x = ()
    x = (file,)
    print(x)
    db.insert(insert_files, x)

    query = "SELECT id from project_files where name = %s"
    print(db.select(query, (file,)))
    return db.select(query, (file,))[0][0]

def run(github_number=None):
    if github_number is not None:
        pulls = []
        pulls.append(target_repo.get_pull(github_number))
        issues = []
        issues.append(target_repo.get_issue(github_number))
    else:
        pulls = target_repo.get_pulls(state='closed', sort='created')
        issues = target_repo.get_issues(state='closed', direction='asc')

    get_pull_requests(pulls)
    get_pull_request_comments(issues)
    get_pull_commits(pulls)
    get_project_commits(pulls)

    print("ALL finish")
