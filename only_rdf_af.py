import json
import glob
import statistics
from natsort import natsorted
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
import sys
from pprint import pprint
import numpy as np
from collections import Counter
import collections
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', 100)  # 10個結果を表示
SUBSET_FEATURE = 10  # 部分空間の次元数
CLASSIFIER_NUM = 100  # 分類器の数
MANHATTAN_DISTANCE = 1  # KNNので採用する距離の種類
K_NEIGHBOR = 1  # KNNのKの数字
COLUMN_DIRECTION = 1  # 列方向指定用の定数
ROW_DIRECTION = 0  # 行方向指定用の定数
labels = []  # 正解ラベル
predicted_labels = []  # 弱い分類器の予測ラベル格納
final_labels = []
# answer_labels = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]  # predicted_labelsの正解
answer_labels = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]  # predicted_labelsの正解
gl_person_num = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]  # ギャラリーのデータ数
pr_person_num = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]  # プローブのデータ数
gallery_feature = pd.DataFrame()  # ギャラリーの特徴量格納
probe_feature = pd.DataFrame()  # プローブの特徴量格納
gl_pr = ["gallery", "probe"]
feature_names = [
    "stDx1", "stDx2", "stDx3", "stDx4", "stDx5", "stDx6", "stDy1", "stDy2", "stDy3",
    "mDx1", "mDx2", "mDx3", "mDx4", "mDx5", "mDx6", "mDy1", "mDy2", "mDy3",
    "Dis0_1", "Dis2_3", "Dis3_4", "Dis1_8", "Dis8_9", "Dis9_10",
    "Dis1_11", "Dis11_12", "Dis12_13", "Dis5_6", "Dis6_7", "Dis1_8and11",
    "Height",
    "u_stDx1", "u_stDx2", "u_stDx3", "u_stDx4", "u_stDx5", "u_stDx6", "u_stDy1", "u_stDy2", "u_stDy3",
    "u_mDx1", "u_mDx2", "u_mDx3", "u_mDx4", "u_mDx5", "u_mDx6", "u_mDy1", "u_mDy2", "u_mDy3"
]  # 10個ランダムに抽出する時のシャッフルするリスト
af_feature_name = [
    "Dis0_1", "Dis2_3", "Dis3_4", "Dis1_8", "Dis8_9", "Dis9_10",
    "Dis1_11", "Dis11_12", "Dis12_13", "Dis5_6", "Dis6_7", "Dis1_8and11",
    "Height",
]
rdf_feature_name = [
    "stDx1", "stDx2", "stDx3", "stDx4", "stDx5", "stDx6", "stDy1", "stDy2", "stDy3",
    "mDx1", "mDx2", "mDx3", "mDx4", "mDx5", "mDx6", "mDy1", "mDy2", "mDy3",
    "u_stDx1", "u_stDx2", "u_stDx3", "u_stDx4", "u_stDx5", "u_stDx6", "u_stDy1", "u_stDy2", "u_stDy3",
    "u_mDx1", "u_mDx2", "u_mDx3", "u_mDx4", "u_mDx5", "u_mDx6", "u_mDy1", "u_mDy2", "u_mDy3"
]
for index in gl_person_num:  # 特徴量データを取り出す
    for g_p in gl_pr:
        files = natsorted(glob.glob("./json/feature_sets/{0}/{1}/*".format(index, g_p)))
        for file in files:
            with open(file) as open_file:
                json_data = json.load(open_file)
                df = pd.DataFrame(json_data)
            if g_p == "gallery":
                labels.append(int(index))  # ギャラリーデータの場合はlabelsにラベルを追加
                gallery_feature = pd.concat([gallery_feature, df], axis=ROW_DIRECTION)
            if g_p == "probe":
                probe_feature = pd.concat([probe_feature, df], axis=ROW_DIRECTION)  # プローブデータを追加

# afを削除する
for feature in rdf_feature_name:
    gallery_feature = gallery_feature.drop(feature, axis=1)
    probe_feature = probe_feature.drop(feature, axis=1)

gallery_feature = gallery_feature.reset_index(drop=True)  # 行名のふり直し
probe_feature = probe_feature.reset_index(drop=True)  # 行名のふり直し
# print(gallery_feature)
# print(probe_feature)


# 分類器の数実行

for i in range(5):
    accuracy_list = []  # 認証精度のリスト
    for k in range(1, 12, 2):
        print("k = {0}".format(k))
        final_labels = []
        for index in pr_person_num:  # プローブの人数分
            predicted_labels = []  # ラベルリストを初期化
            predicted_person = []
            predicted_times = []
            for classifier_num in range(CLASSIFIER_NUM):  # 部分空間数
                gl_selected_feature = gallery_feature.sample(n=SUBSET_FEATURE, axis=COLUMN_DIRECTION)  # ランダムに特徴量を取得
                pr_selected_feature = pd.DataFrame(probe_feature[list(gl_selected_feature.columns)])  # 対象のプローブデータを取得
                pr_selected_feature = pr_selected_feature.loc[[int(index)]]
                subset_classifier = KNeighborsClassifier(n_neighbors=k, p=MANHATTAN_DISTANCE)  # 分類を実行
                subset_classifier.fit(gl_selected_feature, labels)
                predicted_labels.extend(subset_classifier.predict(pr_selected_feature))
            # print("this is weak classifier labels", Counter(predicted_labels).most_common())
            final_labels.append(statistics.mode(predicted_labels))

        # print("this is the answer{0}".format(final_labels))
        recognition_score = accuracy_score(final_labels, answer_labels) * 100  # 正答率を算出
        accuracy_list.append(recognition_score)
    print("The recognition score is {0}\n\n".format(accuracy_list))  # 正答率を出力
