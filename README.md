# piscesとは
+ 有益提案抽出支援システム
+ 過去の議論が終了したPull Request(以下PR)を機械学習に用い，新規のPRを優先的に内容を見るべきか提示する．
+ 提示方法は以下がある．
  + PRに自動でラベルをつけて優先度を示す．
  + WebページにPRの一覧と優先順位を表示する．

## Requirements
+ Python 3.7
+ MySQL

## Install MySQL
自身のOSに従って，以下を実行する．
### Linux
`$ sudo apt install mysql-server mysql-client`

### Mac OS
`$ brew install mysql-server mysql-client`

## Install pisces
以下のコマンドを順に実行する．
```
$ git clone git@github.com:fujiwara-yu/pisces.git
$ cd pisces
$ python -m venv <myenv>
$ source <myenv>/bn/activate
$ pip install -r requirements.txt
```
`<myenv>`は任意の名前

## Setup
### GitHubのアクセストークンを取得
以下を参考にアクセストークンを取得する．
+ [アクセストークンの取得](https://docs.github.com/ja/free-pro-team@latest/github/authenticating-to-github/creating-a-personal-access-token)
+ トークンに付与する権限はrepoを選択

### GitHub Wehooksの設定

1. Webhooksを設定したいプロジェクトのGitHubのリポジトリに移動する．
2. 右上のSettingsを選択する．
3. 左側の一覧からWebhooksを選択する．
4. 右側のAdd webhookを選択する．
5. 設定画面が表示されたら，以下を設定する．
+ Payload URL: POST先のURL
+ Content type: application/json を選択
+ Which events would you like to trigger this webhook?: Let me select individual events を選択
  + Pull Request にチェック
6. Add webhook を選択する．

### mysqlの設定
以下を実行し，mysqlにログインする．
```
$ mysql -u root -p
```

MySQLのコマンドラインから以下を実行し，データベースを作成する．
```
> CREATE DATABASE <database>;
```
`<database>`は作成したいデータベースの名前

### settings.yamlの編集
settings.yaml.sample をsettings.yamlにコピーし，settings.yaml に設定を記述する．
+ token: GitHubのアクセストークンを記述
+ user: 適用するプロジェクトのユーザ名
+ repo: 適用するプロジェクトのリポジトリ名
+ database: PRを保存するデータベース名
+ db_host: データベースの接続先ホスト
+ db_user: データベースのユーザ名

## Launch
### 初回起動の設定
以下のコマンドを実行し，MySQLサーバを起動する．
```
$ mysql.server start
```

以下のコマンドを実行する．
```
$ python bin/main.py init
```
リポジトリのデータ量によっては，トークンの制限に引っ掛かり，数時間程かかることもある．

### 起動
以下のコマンドを実行する．
```
$ python bin/main.py start
```
