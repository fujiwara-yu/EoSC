import sys
import os

app_home = os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)) , ".." ))
sys.path.append(os.path.join(app_home))
sys.path.append(os.path.join(app_home,"lib"))

import re
import datetime
import lib.database
from lib.pullrequest import PullRequestController
import csv

class PullRequestFeature:
    def __init__(self, pr):
        self.github_number = pr.github_number
        self.commits = pr.commits
        self.fix_len = pr.additions + pr.deletions
        self.changed_files = pr.changed_files
        self.file_active = self.file_active_check(pr)
        self.branch_active = self.branch_active_check(pr)
        self.created_at = pr.created_at
        self.useful = self.useful_check(pr)


    #private

    # 有益無益に分類
    # return useful  (有益)
    #        useless (無益)
    def useful_check(self, pr):
        db = lib.database.Database()
        self.github_number = pr.github_number
        # 1.提案が merge されたか
        if pr.merged_at is not None:
            return "useful"

        query = "SELECT * FROM commits WHERE pull_request_id = %s;"
        commits = db.select(query, (str(pr.id),))

        # 2.commit の一部をプロジェクトに反映したか
        for commit in commits:
            if commit[5] == "pull_request_and_project":
                return "useful"

        # 3.commit message での close
        for commit in commits:
            comment = commit[4]
            if re.search(r"(?:fixe[sd]?|close[sd]?|resolve[sd]?)(?:[^\/]*?|and)#([0-9]+)", comment, re.M | re.I):
                return "useful"

        # 4.議論の中に commit id があるか
        # pullsのidからcommentsのデータを取り出して調べる
        query = "SELECT body FROM pull_request_comments WHERE pull_request_id = %s;"
        comment_body = db.select(query, (pr.id,))
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
                query = "SELECT sha FROM commits;"
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
    def file_active_check(self, pr):
        db = lib.database.Database()
        months_back = 3
        query = 'SELECT * FROM commits WHERE pull_request_id = %s;'
        commits = db.select(query, (pr.id,))

        # pr作成日時
        tc = pr.created_at

        # 初期化
        file_list = []
        activity = 0

        start = pr.created_at + datetime.timedelta(days=-30*months_back)
        end = pr.created_at

        # commits_and_files と filesを組み合わせる
        for commit in commits:
            query = "SELECT DISTINCT file_id, name FROM commits_files INNER JOIN project_files ON commits_files.file_id = project_files.id WHERE commit_sha = %s;"
            files = db.select(query, (commit[0],))
            for f in files:
                file_list.append(f)

        for file in file_list:
            # ３ヶ月に限定する
            query = "SELECT DISTINCT sha, created_at FROM commits_files INNER JOIN commits ON commits_files.commit_sha = commits.sha WHERE file_id = %s AND commits.created_at BETWEEN %s AND %s;"
            commit_create_time_list = db.select(query, (file[0],start,end))
            #print(commit_create_time_list)
            for commit_create_time in commit_create_time_list:
                activity = activity + 1.0 - (tc - commit_create_time[1]).total_seconds() / (3600.0 * 24 * 30 * months_back)

        return activity

    # 3ヵ月分のcommitを調べる
    # pullreqに含まれるcommitの変更したブランチを調べる
    # ブランチを変更しているcommitが３ヵ月以内であれば取り出す
    # できてない
    def branch_active_check(self, pr):
        db = lib.database.Database()
        months_back = 3
        tc = pr.created_at
        activity = 0
        branch = pr.branch
        start = pr.created_at + datetime.timedelta(days=-30*months_back)
        end = pr.created_at

        # 3ヵ月いないのをブランチごとに取り出す pr[7]のブランチの情報でwhere
        query = "SELECT DISTINCT sha, commits.created_at FROM pull_requests INNER JOIN commits ON pull_requests.id = commits.pull_request_id WHERE branch = %s AND commits.created_at BETWEEN %s AND %s;"
        commit_list = db.select(query, (branch,start,end))

        for commit in commit_list:
            activity = activity + 1.0 - (tc - commit[1]).total_seconds() / (3600.0 * 24 * 30 * months_back)

        #print(activity)
        return activity

class PullRequestFeatureController:
    def get_pull_request_feature(pr):
        print(f"No. {pr.github_number}")
        prf = PullRequestFeature(pr)
        with open(app_home + '/db/pull_request_feature.csv', 'a') as f:
            writer = csv.writer(f)
            writer.writerow([prf.github_number, prf.commits, prf.fix_len, prf.changed_files, prf.file_active, prf.branch_active, prf.created_at, prf.useful])
        return prf

    def get_pull_request_feature_all():
        with open(app_home + '/db/pull_request_feature.csv', 'w') as f:
            writer = csv.writer(f)
            writer.writerow(["github_number", "commits", "fix_len", "changed_files", "file_active", "branch_active", "created_at", "useful"])

        pull_request_feature_list =[]
        pull_requests = PullRequestController.get_pull_request_all()

        for pr in pull_requests:
            pull_request_feature = PullRequestFeatureController.get_pull_request_feature(pr)
            pull_request_feature_list.append(pull_request_feature)

        return pull_request_feature_list
