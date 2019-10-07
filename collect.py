#!/usr/bin/env python
from github import Github
import sys
import mysql.connector
import time
import types
import yaml

def rate_limit_controll():
    # APIの制限メッセージ
    rate_remaining, rate = client.rate_limiting
    print("limit: %d" % rate_remaining)
    if (rate_remaining < 10):
        print("API limit\nPlease wait 1 hour")
        time.sleep(3600)

#def get_github_data(repo):
#    pulls = repo.get_pulls(state='close', sort='created')
#    store_pulls(pulls)
#
#def store_pulls(pulls):
#    for pr in pulls:
#        print(pr.id, pr.number, pr.user.id, pr.created_at, pr.closed_at, pr.merged_at, pr.state, pr.additions, pr.deletions, pr.changed_files, pr.base.repo.default_branch)

# PRをDBに保存する
def get_pull_list():
    print("Get pull start")
    insert_pulls = "INSERT IGNORE INTO pulls (id, number, username, body, created_at, closed_at, merged_at, state, commits, additions, deletions, changed_files, branch) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
    for pr in pulls:
        p = ()
        p = (pr.id, pr.number, pr.user.login, pr.body, pr.created_at, pr.closed_at, pr.merged_at, pr.state, pr.commits, pr.additions, pr.deletions, pr.changed_files, pr.base.repo.default_branch)
        print(pr.id, pr.number, pr.user.login, pr.body, pr.created_at, pr.closed_at, pr.merged_at, pr.state, pr.commits, pr.additions, pr.deletions, pr.changed_files, pr.base.repo.default_branch)
        cursor.execute(insert_pulls, p)
        db.commit()
        rate_limit_controll()

    print("Get pull finish")
# PRとかのcommentをDBに保存
def get_pull_comment_list():
    print("Get pull_comment start")
    insert_comments = "INSERT IGNORE INTO pullreq_comments (id, pr_id, username, created_at, comment) VALUES (%s, %s, %s, %s, %s);"
    for iss in issues:
        comments = iss.get_comments()
        for prc in comments:
            x = ()
            x = (prc.id, iss.number,prc.user.login, prc.created_at, prc.body)
            print(prc.id, iss.number,prc.user.login, prc.created_at, prc.body)
            cursor.execute(insert_comments, x)
            db.commit()
            rate_limit_controll()

    print("Get pull_comment finish")

def get_project_commit_list():
    print("Get project_commit start")
    insert_commits = "INSERT IGNORE INTO project_commits (sha, username, filename, created_at, comment, additions, deletions, changes) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"
    commits = repo.get_commits()
    for com in commits:
        for file in com.files:
            if com.author is not None:
                print(com.sha, com.author.login, file.filename, com.commit.author.date, com.commit.message, file.additions, file.deletions, file.changes)
                x = ()
                x = (com.sha, com.author.login, file.filename, com.commit.author.date, com.commit.message, file.additions, file.deletions, file.changes)
                cursor.execute(insert_commits, x)
                db.commit()
                rate_limit_controll()

    print("Get project_commit finish")

#def commit():
#    pulls = repo.get_pulls(state='close', sort='created')
#    for pull in pulls:
#        commits = pull.get_commits()
#        for commit in commits:
#            if pull.state == ""
#            print(commit.sha)
#            sql = "UPDATE commits SET pr_id = %s WHERE sha = %s;"
#            cursor.execute(sql, (pull.id, commit.sha))
#            db.commit()
#            rate_limit_controll()

def get_pull_commit_list():
    print("Get pull_commit start")
    insert_commits = "INSERT IGNORE INTO pull_commits (sha, pr_id, username, filename, created_at, comment) VALUES (%s, %s, %s, %s, %s, %s);"
    pulls = repo.get_pulls(state='close', sort='created')
    for pull in pulls:
        commits = pull.get_commits()
        for commit in commits:
            com = repo.get_commit(commit.sha)
            if com.author is not None:
                for file in com.files:
                    print(com.sha, pull.id, com.author.login, file.filename, com.commit.author.date, com.commit.message)
                    x = ()
                    x = (com.sha, pull.id, com.author.login, file.filename, com.commit.author.date, com.commit.message)
                    cursor.execute(insert_commits, x)
                    db.commit()
                    rate_limit_controll()

    print("Get pull_commit finish")

def get_pull_title():
    print("Get title start")
    insert_pulls = "INSERT IGNORE INTO title (id, number, title, url) VALUES (%s, %s, %s, %s);"
    for pr in pulls:
        p = ()
        p = (pr.id, pr.number, pr.title, pr.html_url)
        print(pr.id, pr.number, pr.title, pr.html_url)
        cursor.execute(insert_pulls, p)
        db.commit()
        rate_limit_controll()

    print("Get title finish")

def run():
    get_pull_list()
    get_pull_comment_list()
    get_project_commit_list()
    commit()
    get_pull_commit_list()
    get_pull_title()
    print("ALL finish")

if __name__ == "__main__":
    args = sys.argv

     # 引数ないとき
    if(len(args) != 2):
        print("Not argument")
        sys.exit()

    f = open("settings.yaml", "r")
    settings = yaml.load(f)

    #データベース設定
    db=mysql.connector.connect(host="localhost", user="test")

    cursor=db.cursor()

    cursor.execute("USE test_db")
    db.commit()

    token = settings["token"]
    client = Github(token, per_page=100)
    repo = client.get_repo(args[1])
    pulls = repo.get_pulls(state='close', sort='created')
    issues = repo.get_issues(state='closed')
    run()
