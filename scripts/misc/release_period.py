import json
import datetime

with open('data/bootstrap_releases.json') as f:
    data = json.load(f)

previous = 0
for d in reversed(data):
    created_at = d["created_at"]
    print("-----")
    print(d["tag_name"])
    print(created_at)
    created_at = datetime.datetime.strptime(created_at, '%Y-%m-%dT%H:%M:%SZ')
    if previous != 0:
        sub = created_at - previous
        print(sub)

    previous = created_at 

print("-----")
