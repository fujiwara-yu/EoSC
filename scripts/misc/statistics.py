import pandas as pd
import sys

if len(sys.argv) != 2:
    print("No argument len")
    sys.exit()

project = sys.argv[1]

file_name = f"scripts/data/{project}_full.csv"
df = pd.read_csv(file_name)

# 5 3 4 2 1
print(df.describe())

df.plot.box()