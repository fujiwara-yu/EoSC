import numpy as np
import pandas as pd
import joblib
import sys
import numpy as np
import pandas as pd
from sklearn import metrics
import joblib
from sklearn.metrics import classification_report
import sys
from sklearn.metrics import confusion_matrix

# 引数でプロジェクト名指定
if len(sys.argv) != 2:
    print("No argument len")
    sys.exit()

project = sys.argv[1]


use = joblib.load(f"scripts/result/{project}_2.pkl")
use = pd.DataFrame(use)

l =[]
for i, u in use.iterrows():
    if u["hyouka_2"] == 1.0 and u["useful"] == "useful":
        l.append("useful")
    elif u["hyouka_2"] == 1.0 and u["useful"] == "useless":
        l.append("useless")
    elif u["hyouka_2"] == 0.0 and u["useful"] == "useless":
        l.append("useful")
    elif u["hyouka_2"] == 0.0 and u["useful"] == "useful":
        l.append("useless")

result_predict = np.array(l)
predict_label = use["useful"]

accuracy = metrics.accuracy_score(predict_label, result_predict)
print("Accuracy:", accuracy)

#                     Predicted
#                 Negative  Positive
#Actual Negative     TN        FP
#       Positive     FN        TP
print(confusion_matrix(predict_label, result_predict, labels=['useless', 'useful']))

print(classification_report(predict_label, result_predict))