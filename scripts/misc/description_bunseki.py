import pandas as pd
import sys

# 引数でプロジェクト名指定
if len(sys.argv) != 2:
    print("No argument len")
    sys.exit()

project = sys.argv[1]

file_name = f"scripts/result/body_len_{project}.csv"
df = pd.read_csv(file_name)

file_name = f"scripts/data/{project}_full.csv"
df_full = pd.read_csv(file_name)
df_merged = pd.merge(df_full, df, left_on="github_id", right_on="number")

print(df_merged.describe())

df_useful = df_merged.copy()
index_useful = df_useful[ df_useful["useful"] == "useless" ].index
df_useful.drop(index_useful, inplace=True)

index_useless = df_merged[ df_merged["useful"] == "useful" ].index
df_useless = df_merged.drop(index_useless)

#print(df_useful)
#print(df_useless)
print(df_useful.describe())
print(df_useless.describe())
