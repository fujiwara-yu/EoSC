# EoSCとは
+ Extraction of Significant Contributions　の略
+ 有益提案の抽出支援システム

# プログラムの説明
+ bunkatsu.py
    分割日時を指定して，learn_file.csvのデータをtrain_bunkatsu.csv(学習用データ)とpredict_bunkatsu.csv(判定用データ)に分割する．
    分割結果から，学習と判定を行う．

+ collect.py
    GitHubリポジトリからデータを集めてDB(MySQL)に保存する．

+ create_learn_file.py
    DBからデータを取り出して，learn_file.csv(PRのデータが入っているファイル)を作成する．

+ db_create.py
    MySQLのテーブルを作成する．

+ hantei.py
    判定データの有益な確率を算出する．

+ randomforest.py
    学習データからランダムフォレスを行い，学習済みモデルを作成する．

+ server.py
    学習結果を表示するサーバを立てる．

# セットアップ
## 実行環境の設定
+ `$ pythom -m venv <myenv>`
+ `$ source <myenv>/bin/activate`
+ `$ pip install -r requirements.txt`
    + ※<myenv>は任意の名前

## mysqlの設定
+ yamlにdbの設定を記述
+ 以下を実行する．
`$ python db_create`

# 実行
## mysqlの実行
+ mysql.server start

## プログラムの実行
### PRのデータファイルの作成
+ `$ python collect.py`
+ `$ python create_learn_file.py`

### PRのデータファイルの分割，学習，および判定
+ `$ python bunkatsu.py <time>`
    + ※<time>は YYYY-MM-DD で指定
    + 例) `$ python bunkatsu.py 2019-01-01`

### PRのデータファイルの表示
ローカルにWebサーバを立てて，判定したPR一覧を表示する．
+ `$ python server.py`

# 作成中の機能
+ WebhookまたはGitHub apiのeventを呼び出して自動でPRを集める機能
+ 判定結果から対応するラベルをPRに付与する機能
