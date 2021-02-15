import sys
import os

app_home = os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)) , ".." ))
sys.path.append(os.path.join(app_home))
sys.path.append(os.path.join(app_home,"lib"))

from github import Github
import yaml

# yamlファイルの読み込み

f = open(app_home + "/settings.yaml", "r")
settings = yaml.load(f, Loader=yaml.SafeLoader)
# tokenの設定
token = settings["token"]

# 引数でプロジェクト名指定
if len(sys.argv) != 3:
    print("No argument len")
    sys.exit()

user = sys.argv[1]
repo = sys.argv[2]

user_repo = user + "/" + repo
client = Github(token, per_page=100)
target_repo = client.get_repo(user_repo)

pulls = target_repo.get_pulls(state='closed', sort='created')

with open(f"scripts/result/body_len_{repo}.csv", "w") as f:
    f.write("number,body_len\n")

count = 0
for pull in pulls:
    if pull.body is not None:
        number = pull.number
        body = pull.body
        body_len = len(body)
        #print(f"{number},{body_len},{body}")
        with open(f"scripts/result/body_len_{repo}.csv", "a") as f:
            f.write(f"{number},{body_len}\n")
        count += body_len

print(count)
