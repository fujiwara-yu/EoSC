import sys
import pandas as pd
import randomforest
import hantei
import datetime

## データを学習用と判定用に分割するプログラム
## デモ用

# 素性とか含めたファイル読み込み
path = 'learn_file.csv'
df = pd.read_csv(path)

# 作成日時をdatetime型に変換
df["created_at"] = pd.to_datetime(df["created_at"])

# コマンドライン引数から日付を受け付けてdatetime型に変換
args = sys.argv
sep_datetime = datetime.datetime.strptime(args[1], '%Y-%m-%d')

# 読み込んだデータを分割
train = df[df["created_at"] <= sep_datetime]
predict = df[df["created_at"] > sep_datetime]

# randomforest.py に渡すファイルを作成して渡す
train = train.drop_duplicates('requester', keep='first')
train.to_csv("train_bunkatsu.csv", index=False)
randomforest.randomforest("train_bunkatsu.csv")

# hantei.py に渡すファイルを作成して渡す
predict.to_csv("predict_bunkatsu.csv", index=False)
hantei.hantei("predict_bunkatsu.csv")
