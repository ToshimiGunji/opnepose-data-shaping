import json
import glob
import sys
from pprint import pprint
import statistics
from natsort import natsorted
import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

pd.set_option('display.max_columns', 10)  # 10個結果を表示
SUBSET_FEATURE = 10  # 部分空間の次元数
CLASSIFIER_NUM = 100  # 分類器の数
gl_files = natsorted(glob.glob("./feature_sets/gallery/*"))  # ギャラリーデータファイル
pr_files = natsorted(glob.glob("./feature_sets/probe/*"))  # プロ―ブデータファイル
labels = []  # 正解ラベル
predicted_labels = []  # 弱い分類器の予測ラベル格納
final_labels = []
# answer_labels = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]  # predicted_labelsの正解
answer_labels = [0, 1]  # predicted_labelsの正解
gl_person_num = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]  # ギャラリーのデータ数
pr_person_num = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]  # プローブのデータ数
gallery_feature = pd.DataFrame()  # ギャラリーの特徴量格納
probe_feature = pd.DataFrame()  # プローブの特徴量格納
gl_pr = ["gallery", "probe"]
feature_names = ["stDx1", "stDx2", "stDx3", "stDx4", "stDx5", "stDx6", "stDy1", "stDy2", "stDy3",
                 "mDx1", "mDx2", "mDx3", "mDx4", "mDx5", "mDx6", "mDy1", "mDy2", "mDy3",
                 "Dis0_1", "Dis2_3", "Dis3_4", "Dis1_8", "Dis8_9", "Dis9_10",
                 "Dis1_11", "Dis11_12", "Dis12_13", "Dis5_6", "Dis6_7", "Dis1_8and11",
                 "Height",
                 "u_stDx1", "u_stDx2", "u_stDx3", "u_stDx4", "u_stDx5", "u_stDx6", "u_stDy1", "u_stDy2", "u_stDy3",
                 "u_mDx1", "u_mDx2", "u_mDx3", "u_mDx4", "u_mDx5", "u_mDx6", "u_mDy1", "u_mDy2", "u_mDy3"
                 ]  # 10個ランダムに抽出する時のシャッフルするリスト

for index in gl_person_num:  # 特徴量データを取り出す
    for g_p in gl_pr:
        files = natsorted(glob.glob("./json/feature_sets/{0}/{1}/*".format(index, g_p)))
        for file in files:
            with open(file) as open_file:
                json_data = json.load(open_file)
                df = pd.DataFrame(json_data)
            if g_p == "gallery":
                labels.append(int(index))  # ギャラリーデータの場合はlabelsにラベルを追加
                gallery_feature = pd.concat([gallery_feature, df], axis=0)
            if g_p == "probe":
                probe_feature = pd.concat([probe_feature, df], axis=0)  # プローブデータを追加
    if index == "1":
        break

# 行名のふり直し
gallery_feature = gallery_feature.reset_index(drop=True)
probe_feature = probe_feature.reset_index(drop=True)

# 分類器の数実行
for index in pr_person_num:  # プローブの人数分
    predicted_labels = []  # ラベルリストを初期化
    for classifier in range(CLASSIFIER_NUM):  # 部分空間数
        # ランダムに特徴量を取得
        gl_selected_feature = gallery_feature.sample(n=10, axis=1)
        print("This is gallery data\n", gl_selected_feature)
        # 対象のプローブデータを取得
        pr_selected_feature = pd.DataFrame(probe_feature[list(gl_selected_feature.columns)])
        pr_selected_feature = pr_selected_feature.loc[[int(index)]]
        print("\nThis is probe selected data\n", pr_selected_feature)

        # 分類を実行
        subset_classifier = KNeighborsClassifier(n_neighbors=1, p=1)
        subset_classifier.fit(gl_selected_feature, labels)
        print("This data is classified as {0} \n".format(subset_classifier.predict(pr_selected_feature)))
        predicted_labels.extend(subset_classifier.predict(pr_selected_feature))
        print("this is weak classifier labels", predicted_labels)
        if classifier == 4:
            break
    final_labels.append(statistics.mode(predicted_labels))
    print("this is the answer{0}\n\n".format(final_labels))
    if index == "1":
        break

# 正答率を算出
# recognition_score = accuracy_score(final_labels, answer_labels)*100
# print("The recognition score is {0}".format(recognition_score))
