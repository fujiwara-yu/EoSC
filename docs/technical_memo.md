# Technical Memo

## ディレクトリ構成
```
.
├── MySQL_dump
│   ├── angularjs.dump
│   ├── bootstrap.dump
│   ├── jquery.dump
│   └── rails.dump
├── README.md
├── bin
│   └── main.py
├── lib
│   ├── collect.py
│   ├── create_db.py
│   ├── database.py
│   ├── predict.py
│   ├── pullrequest.py
│   ├── pullrequestfeature.py
│   └── randomforest.py
├── requirements.txt
├── scripts
│   ├── README.md
│   ├── data
│   │   └── bootstrap_releases.json
│   ├── evaluation_accuracy
│   │   ├── evaluation.py
│   │   ├── evaluation_short.py
│   │   ├── pickle_plot.py
│   │   ├── pickle_plot_month_all.py
│   │   └── result
│   │       ├── angularjs_result.txt
│   │       ├── bootstrap_result.txt
│   │       ├── jquery_result.txt
│   │       └── rails_result.txt
│   ├── evaluation_ap
│   │   ├── evaluation_ap.sh
│   │   ├── evaluation_ap_no_series.py
│   │   ├── evaluation_ap_no_series.sh
│   │   ├── pickle_ap_first_user.py
│   │   └── result
│   │       ├── angularjs_result.txt
│   │       ├── bootstrap_result.txt
│   │       ├── jquery_result.txt
│   │       └── rails_result.txt
│   ├── evaluation_feature_importance
│   │   ├── evaluation_ap_feature_3.py
│   │   ├── evaluation_feature_importance.py
│   │   ├── evaluation_feature_importance.sh
│   │   ├── evaluation_new_feature.sh
│   │   └── result
│   │       ├── angularjs_result.txt
│   │       ├── angularjs_result_old_f5.txt
│   │       ├── bootstrap_result.txt
│   │       ├── bootstrap_result_old_f5.txt
│   │       ├── jquery_result.txt
│   │       ├── jquery_result_old_f5.txt
│   │       ├── rails_result.txt
│   │       └── rails_result_old_f5.txt
│   ├── evaluation_new_feature
│   │   ├── evaluation_new_feature.py
│   │   ├── evaluation_new_feature.sh
│   │   ├── join_new_feature.py
│   │   ├── pickle_ap_core_user.py
│   │   ├── pickle_ap_first_user.py
│   │   ├── pickle_plot_kanseiban.py
│   │   ├── result_4f
│   │   │   ├── angularjs_result_f_new.txt
│   │   │   ├── bootstrap_result_f_new.txt
│   │   │   ├── jquery_result_f_new.txt
│   │   │   └── rails_result_f_new.txt
│   │   └── result_5f
│   │       ├── angularjs_result_f_new.txt
│   │       ├── bootstrap_result_f_new.txt
│   │       ├── jquery_result_f_new.txt
│   │       └── rails_result_f_new.txt
│   ├── evaluation_new_feature_3f
│   │   ├── evaluation_new_feature.py
│   │   ├── pickle_ap_first_user.py
│   │   └── result
│   │       ├── angularjs_result_f_new.txt
│   │       ├── bootstrap_result_f_new.txt
│   │       ├── jquery_result_f_new.txt
│   │       └── rails_result_f_new.txt
│   ├── evaluation_old_feature_3f
│   │   ├── evaluation_old_feature.py
│   │   ├── evaluation_old_feature_3f.sh
│   │   ├── pickle_ap_first_user.py
│   │   └── result
│   │       ├── angularjs_result_f_new.txt
│   │       ├── bootstrap_result_f_new.txt
│   │       ├── jquery_result_f_new.txt
│   │       └── rails_result_f_new.txt
│   ├── misc
│   │   ├── bootstrap_releases.txt
│   │   ├── bootstrap_result.txt
│   │   ├── classification.py
│   │   ├── description.py
│   │   ├── description_bunseki.py
│   │   ├── evaluation.py
│   │   ├── evaluation_not_use_datetime.py
│   │   ├── evaluation_test.py
│   │   ├── pickle_ap_core_user.py
│   │   ├── pickle_ap_first_user.py
│   │   ├── pickle_ap_mix.py
│   │   ├── pickle_ap_test.py
│   │   ├── pickle_plot_idouheikin.py
│   │   ├── pickle_plot_idouheikin2.py
│   │   ├── pickle_plot_kanseiban_feature.py
│   │   ├── pickle_plot_month.py
│   │   ├── pickle_plot_month_all.py
│   │   ├── pickle_plot_precision.py
│   │   ├── pr_active.py
│   │   ├── release_period.py
│   │   └── statistics.py
│   └── result
│       ├── angularjs_result.txt
│       ├── bootstrap_result.txt
│       ├── bootstrap_result_f_new.txt
│       ├── jquery_result.txt
│       ├── jquery_result_f_new.txt
│       └── rails_result.txt
├── settings.yaml.sample
└── web
    ├── server.py
    ├── static
    │   └── style.css
    └── templates
        └── index.html
```

+ 主要なディレクトリ/ファイルの一覧

   | 通番 | ファイル(ディレクトリ)名      | 説明                                                |
   |------|-------------------------------|-----------------------------------------------------|
   |    1 | bin/                          | 実行ファイルを配置している．          |
   |    2 | db/           | システムで使用されるデータが保存される． |
   |    3 | docs/                 | 本ディレクトリ．ドキュメントを配置している．                      |
   |    4 | lib/ | ライブラリとして使用するプログラムを配置している． |
   |    5 | MySQL_dump/                     | 本システムで収集してMySQLに保存していたデータを配置している．            |
   |    6 | scripts/        | 評価プログラムを配置している．|
   |    7 | web/        | GitHubとの連携，Web上でのPR一覧の表示に関わるプログラムを設置している．  |
   |    8 | requirements.txt | インストールするパッケージ一覧が書いてある． |
   |    9 | settings.yaml.sample                        | 本システムを実行させるのに必要な設定ファイルのサンプル． |


## その他
### 評価に用いたデータの収集方法
+ GHTorrent
  + 以下の資料を参照
  + http://lastnote.swlab.cs.okayama-u.ac.jp/document/show/gn/257-05

+ 本システム
  + 設定したプロジェクトのデータを収集可能

### 評価に用いたデータ
+ GHTorrentから収集したデータを用いて評価
+ 新しい素性を追加する際に本システムからデータを収集し，既存のデータと結合した．

### その他，研究する際に検討した方が良いと考えること
+ 藤原の研究で使用したデータは2016年までのデータのため新しく収集した方がいいかも
+ 新しく対象のプロジェクトを決めてもいいかも
+ 学習のハイパーパラメータは決め打ちです
+ 本システムを改良する場合，Python部分でAPIを提供して，表示部でvue.jsやReactを用いた方が改良しやすいかも
+ ラベル付けの条件をしっかりと検討できていないため，ラベル付けの条件は十分に検討してください
