import sys
import os

app_home = os.path.abspath(os.path.join( os.path.dirname(os.path.abspath(__file__)) , ".." ))
sys.path.append(os.path.join(app_home))
sys.path.append(os.path.join(app_home,"lib"))

from lib.pullrequestfeature import PullRequestFeatureController
import click
import web.server
import collect
import predict
import create_db
import randomforest

@click.group()
def cmd():
    pass

# TODO: pull_request_feature_listの保存をした方がいい
# とりあえずPullRequestFeatureControllerで保存
@cmd.command()
def init():
    #create_db.create_db()
    #collect.run()
    pull_request_feature_list = PullRequestFeatureController.get_pull_request_feature_all()
    randomforest.randomforest(pull_request_feature_list)
    predict.opened_all()

@cmd.command()
def start():
    web.server.start()

def main():
    cmd()

if __name__ == "__main__":
    main()
