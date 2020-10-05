# piscesとは
+ 有益提案の抽出支援システム
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
`$ git clone git@github.com:fujiwara-yu/pisces.git`
`$ cd pisces`
`$ python -m venv <myenv>`
`$ source <myenv>/bn/activate`
`$ pip install -r requirements.txt`
<myenv>は任意の名前

## Setup
### GitHubのアクセストークンを取得
以下を参考にアクセストークンを取得する．
+ [アクセストークンの取得](https://docs.github.com/ja/free-pro-team@latest/github/authenticating-to-github/creating-a-personal-access-token)
+ トークンに付与する権限はrepoを選択前

### mysqlの設定
TODO

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
以下のコマンドを実行する．
`$ python bin/main.py init`

リポジトリの大きさによっては，トークンの制限に引っ掛かり，数時間程かかることもある．

### 起動
以下のコマンドを実行する．
`$ python bin/main.py start`

## Uninstall
TODO
