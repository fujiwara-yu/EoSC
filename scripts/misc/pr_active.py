import datetime

# データベースからデータをとって算出

def pr_branch_active_check(self, pr):
        db = lib.database.Database()
        months_back = 3
        tc = pr.created_at
        activity = 0
        branch = pr.branch
        start = pr.created_at + datetime.timedelta(days=-30*months_back)
        end = pr.created_at

        query = "SELECT created_at FROM pull_requests WHERE branch = %s AND created_at BETWEEN %s AND %s;"
        pulls = db.select(query, (branch,start,end))

        for pull in pulls:
            activity = activity + 1.0 - (tc - pull[0]).total_seconds() / (3600.0 * 24 * 30 * months_back)

        return activity

def pr_file_active_check(self, pr):
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

    # ファイル一覧の作成
    for commit in commits:
        query = "SELECT DISTINCT file_id FROM commits_files WHERE commit_sha = %s;"
        files = db.select(query, (commit[0],))
        for f in files:
            file_list.append(f[0])

    for file in file_list:
        #対象期間のpr取り出し
        query = "SELECT pull_requests.created_at FROM pull_requests INNER JOIN commits ON pull_requests.id = commits.pr_id INNER JOIN commits_files ON commits.sha = commts_files.commit_sha WHERE created_at BETWEEN %s AND %s;"
        pr_create_time_list = db.select(query, (file[0],start,end))
        for pr_create_time in pr_create_time_list:
            activity = activity + 1.0 - (tc - pr_create_time[0]).total_seconds() / (3600.0 * 24 * 30 * months_back)

    return activity
