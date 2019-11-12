#!/usr/bin/env python
import sys
import mysql.connector
import re
import time
import datetime
from dateutil.relativedelta import relativedelta
import lib.database

db = lib.database.Database()

# データを取得
def get_data():
    return db.select('SELECT * FROM pulls join title on pulls.id = title.id')

# 有益無益に分類
def useful_check(row):
    # 1.提案が merge されたか
    if row[6] is not None:
        return "useful"

    query = "SELECT * FROM pull_commits WHERE pr_id = %s;"
    commits = db.select(query, (str(row[0]),))

    # 2.commit の一部をプロジェクトに反映したか
    #for commit in commits:
    #    if commit is not None:
    #        return "2.useful"

    # project pull commit の場合
    # pro pull から同一のshaを取り出して比較
    query = "SELECT * FROM project_commits WHERE sha = %s;"
    for commit in commits:
        sha = db.select(query, (str(commit[0]),))
        if sha != []:
            return "useful"

    # 3.commit message での close
    for commit in commits:
        comment = commit[5]
        if re.search(r"(?:fixe[sd]?|close[sd]?|resolve[sd]?)(?:[^\/]*?|and)#([0-9]+)", comment, re.M | re.I):
            return "useful"

    # 4.議論の中に commit id があるか
    # pullsのidからcommentsのデータを取り出して調べる
    query = "SELECT comment FROM pullreq_comments WHERE pr_id = %s;"
    comment_body = db.select(query, (row[1],))
    if len(comment_body) == 0: 
        last = "Not match"
    elif len(comment_body) == 1:
        last = comment_body[0]
    elif len(comment_body) == 2:
        last_list = comment_body[0] + comment_body[1]
        last = ",".join(last_list) 
    else:
        l = len(comment_body)
        last_list = comment_body[l-1] + comment_body[l-2] + comment_body[l-3]
        last = ",".join(last_list)
    # last は pull request の comment の最後から3つ
    list = re.findall(r"[0-9a-f]{6,40}", str(last), re.M)
    if list is not None:
        if re.search(r"merg(?:ing|ed)|appl(?:ying|ed)|pull(?:ing|ed)|push(?:ing|ed)|integrat(?:ing|ed)", str(last), re.IGNORECASE):
            return "useful"
        else:
            query = "SELECT sha FROM project_commits;"
            y = db.select(query)
            if y != []:
                for l in list:
                    if l in str(y):
                        return "useful"

    # 上記を満たさない
    return "useless"


# 3ヵ月分のcommitを調べる
# pullreqに含まれるcommitの変更したファイルを調べる
# ファイルを変更しているcommitが３ヵ月以内であれば取り出す
def commits_on_files_touched(pr):
    months_back = 3
    query = 'SELECT * FROM pull_commits WHERE pr_id = %s;'
    commits = db.select(query, (pr[0],))
    tc = pr[4]
    file_list = []
    com = []

    for commit in commits:
        query = "SELECT filename FROM project_commits WHERE sha = %s;"
        file_list = db.select(query, (commit[0],))

    for file in file_list:
        # ３ヶ月に限定する
        query = "SELECT * FROM project_commits WHERE filename = %s;"
        com = db.select(query, (file[0],))

    activity = 0
    for c in com:
        activity = activity + 1.0 - (tc - c[3]).total_seconds() / (3600.0 * 24 * 30 * months_back)

    #print(activity)
    return activity

# 3ヵ月分のcommitを調べる
# pullreqに含まれるcommitの変更したブランチを調べる
# ブランチを変更しているcommitが３ヵ月以内であれば取り出す
# できてない
def branch_hotness(pr):
    months_back = 3
    # query = 'SELECT * FROM pull_commits WHERE pr_id = %s;'
    # cursor.execute(query, (pr[0],))
    # commits = cursor.fetchall()
    tc = pr[4]
    com = []

    # 3ヵ月いないのをブランチごとに取り出す pr[7]のブランチの情報でwhere
    query = "SELECT * FROM project_commits;"
    com = db.select(query)

    activity = 0
    for c in com:
        activity = activity + 1.0 - (tc - c[3]).total_seconds() / (3600.0 * 24 * 30 * months_back)

    #print(activity)
    return activity

def main():
    path = 'learn_file.csv'
    pulls = get_data()
    #有益無益に分類
    s = "github_id,useful,requester,num_commits_open,lines_modified_open,files_modified_open,commits_on_files_touched,branch_hotness,created_at,title,url\n"
    with open(path, mode='w') as f:
        f.write(s)

    for pull in pulls:
        #print("%d " % pull[1], end="")
        useful = useful_check(pull)
        commit_touched = commits_on_files_touched(pull)
        hotness = branch_hotness(pull)
        print(pull[1], useful, pull[2], pull[8], pull[9]+pull[10],pull[11], commit_touched, hotness, pull[4],pull[15],pull[16])
        s = f"{pull[1]},{useful},{pull[2]},{pull[8]},{pull[9]+pull[10]},{pull[11]},{commit_touched},{hotness},{pull[4]},\"{pull[15]}\",{pull[16]}\n"
        with open(path, mode='a') as f:
            f.write(s)

        with open(path) as f:
            print(f.read())
# New file

if __name__ == "__main__":
    main()