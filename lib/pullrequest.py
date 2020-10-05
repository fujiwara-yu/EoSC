import lib.database

class PullRequest:
    def __init__(self, id, github_number, name, creator_name, body, created_at, closed_at, merged_at, state, commits, additions, deletions, changed_files, branch):
        self.id = id
        self.github_number = github_number
        self.name = name
        self.creator_name = creator_name
        self.body = body
        self.created_at = created_at
        self.closed_at = closed_at
        self.merged_at = merged_at
        self.state = state
        self.commits = commits
        self.additions = additions
        self.deletions = deletions
        self.changed_files = changed_files
        self.branch = branch

class PullRequestController:
    def get_pull_request_all():
        pull_request_list = []
        db = lib.database.Database()
        query = 'SELECT * FROM pull_requests'
        pull_requests = db.select(query)
        for pr in pull_requests:
            p = lib.pullrequest.PullRequest(*pr)
            pull_request_list.append(p)

        return pull_request_list

    def get_pull_request(github_number):
        db = lib.database.Database()
        query = 'SELECT * FROM pull_requests where github_number=%s'
        pr = db.select(query, (github_number,))

        return PullRequest(*pr)
