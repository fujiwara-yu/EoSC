#!/usr/bin/env python
from github import Github
import sys
import mysql.connector
import time
import types
import yaml
import lib.database

def rate_limit_controll():
    # APIの制限メッセージ
    rate_remaining = client.rate_limiting
    print(f"limit: {rate_remaining}")
    if (rate_remaining[0] < 10):
        print("API limit\nPlease wait 1 hour")
        time.sleep(3600)

# PRをDBに保存する
def get_pull_requests():
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
def get_pull_request_comments():
    print("Get pull_request_comments start")
    insert_comments = "INSERT IGNORE INTO pull_request_comments (id, pull_request_id, creator_name, created_at, body) VALUES (%s, %s, %s, %s, %s);"
    issues = target_repo.get_issues(state='closed')
    for iss in issues:
        comments = iss.get_comments()
        for prc in comments:
            insert_data = ()
            insert_data = (prc.id, iss.number, prc.user.login, prc.created_at, prc.body)
            print(insert_data)
            db.insert(insert_comments, insert_data)
            rate_limit_controll()

    print("Get pull_comment finish")

def get_pull_commits():
    print("Get pull_commits start")
    insert_commits = "INSERT IGNORE INTO commits (sha, pull_request_id, creator_name, created_at, body, state) VALUES (%s, %s, %s, %s, %s, %s);"
    #pulls = repo.get_pulls(state='close', sort='created')
    state = "pull_request"
    for pull in pulls:
        commits = pull.get_commits()
        for commit in commits:
            com = target_repo.get_commit(commit.sha)
            if com.author is not None:
                insert_data = ()
                insert_data = (com.sha, pull.id, com.author.login, com.commit.author.date, com.commit.message, state)
                print(insert_data)
                db.insert(insert_commits, insert_data)
                rate_limit_controll()

                for file in com.files:
                    file_id = add_file(file.filename)
                    get_commits_files(com.sha, file_id)

    print("Get pull_commit finish")

def get_project_commits():
    print("Get project_commits start")
    insert_commits = "INSERT IGNORE INTO commits (sha, pull_request_id, creator_name, created_at, body, state) VALUES (%s, %s, %s, %s, %s, %s);"
    commits = target_repo.get_commits()
    state = "project"
    for com in commits:
        if com.author is not None:
            insert_data = ()
            insert_data = (com.sha, None, com.author.login, com.commit.author.date, com.commit.message, state)
            print(insert_data)

            query = "UPDATE commits SET state=%s WHERE sha=%s"
            db.insert(query, ('pull_request_and_project', com.sha))
            db.insert(insert_commits, insert_data)
            rate_limit_controll()

            for file in com.files:
                file_id = add_file(file.filename)
                get_commits_files(com.sha, file_id)

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

def run():
    get_pull_requests()
    get_pull_request_comments()
    get_pull_commits()
    get_project_commits()

    print("ALL finish")

if __name__ == "__main__":
    ## FIX: 引数をyamlから読むようにかえる

    # yamlファイルの読み込み
    f = open("settings.yaml", "r")
    settings = yaml.load(f, Loader=yaml.SafeLoader)

    # DB接続
    db = lib.database.Database()

    # tokenの設定
    token = settings["token"]

    # データを収集するリポジトリの設定
    user = settings["user"]
    repo = settings["repo"]
    user_repo = user + "/" + repo

    client = Github(token, per_page=100)
    target_repo = client.get_repo(user_repo)
    
    # pullsをidから1つだけ指定できれば，closedになったPRを保存できる
    # issuesもかな
    pulls = target_repo.get_pulls(state='closed', sort='created')

    run()
