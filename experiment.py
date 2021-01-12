import json
import glob
import collections as cl
import sys
from pprint import pprint
from natsort import natsorted
import pandas as pd
import numpy as np
from numpy import nan
import os
# pd.set_option('display.max_columns', 100)


from sklearn.model_selection import train_test_split

# アヤメデータセット読み込み
from sklearn.datasets import load_iris

iris = load_iris()

# 特徴量
X = iris.data
# 目的変数
Y = iris.target

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, random_state=0)

from sklearn.neighbors import KNeighborsClassifier

list_nn = []
list_score = []
for k in range(1, 31):  # K = 1~30
    # KNeighborsClassifier
    knc = KNeighborsClassifier(n_neighbors=k)
    knc.fit(X_train, Y_train)
    # 予測　
    Y_pred = knc.predict(X_test)
    # 評価 R^2
    score = knc.score(X_test, Y_test)
    print("[%d] score: {:.2f}".format(score) % k)

print(X_train)