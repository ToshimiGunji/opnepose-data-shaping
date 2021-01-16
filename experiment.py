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
import statistics
# pd.set_option('display.max_columns', 100)
import random
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris
from sklearn.neighbors import KNeighborsClassifier

aa = ["a", "b", "c", "d", "e"]
bb = ["e", "f", "g"]
a = [1, 1, 0, 0, 2, 3, 4, 5]
print(statistics.mode(a))

sys.exit()

target_path = './json/feature_sets/0/gallery/feature_0.json'
target_path2 = './json/feature_sets/0/gallery/feature_1.json'
df1 = pd.DataFrame()
df2 = pd.DataFrame()
with open(target_path) as open_file:
    json_data = json.load(open_file)
    df1 = pd.DataFrame(json_data)
    print(df1)

with open(target_path2) as open_file:
    json_data = json.load(open_file)
    df2 = pd.DataFrame(json_data)
    print(df2)
df_all = pd.concat([df1, df2], axis=0)
df_all = df_all.reset_index(drop=True)
print(df_all)

# KNeighborsClassifier
knc = KNeighborsClassifier(n_neighbors=1, p=1)
knc.fit(df_all, [0, 1])
# 予測　
Y_pred = knc.predict(df1)
print(Y_pred)
# 評価 R^2
# score = knc.score(X_test, Y_test)
