import json
import glob
import collections as cl
import sys
from pprint import pprint
from natsort import natsorted
import pandas as pd
import numpy as np
from numpy import abs
from numpy import nan
from math import sqrt
from sklearn.neighbors import KNeighborsClassifier

gl_files = natsorted(glob.glob("./feature_sets/gallery/*"))  # ギャラリーデータファイル
pr_files = natsorted(glob.glob("./feature_sets/probe/*"))  # プロ―ブデータファイル

SUBSET_DIM = 10  # 部分空間の次元数
SUBSET_NUM = 100  # 分類器の数
gl_df = pd.DataFrame()  # ギャラリーデータ
pr_df = pd.DataFrame()  # プローブデータ
weak_labels = []  # 弱い分類器の予想ラベル格納

x = np.array([[6, 0, 0], [3, 4, 0]])
y = np.array([0, 1])
z = np.array([0, 0, 0])

neigh = KNeighborsClassifier(n_neighbors=1, p=1)
neigh.fit(x, y)
print(neigh.predict([z]))

# 分類器の数実行
for i in range(SUBSET_NUM):
    for file in gl_files:
        print(i)
