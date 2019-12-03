class Pullrequest:
    def __init__(self, pr_id, number, username, body, created_at, closed_at, merged_at, state, commits, additions, deletions, changed_files, branch):
        self.pr_id = pr_id
        self.number = number
        self.username = username
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