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


def get_distance(x1, y1, x2, y2):
    dis = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return dis


pd.set_option('display.max_columns', 100)
files = natsorted(glob.glob("./shaped_json/0/*"))
feature_df = pd.DataFrame({"Dx1": [], "Dx2": [], "Dx3": [], "Dx4": [], "Dx5": [], "Dx6": [],
                           "Dy1": [], "Dy2": [], "Dy3": [],
                           "Dis0_1": [], "Dis2_3": [], "Dis3_4": [], "Dis1_8": [], "Dis8_9": [], "Dis9_10": [],
                           "Dis1_11": [], "Dis11_12": [], "Dis12_13": [], "Dis5_6": [], "Dis6_7": [], "Dis1_8and11": [],
                           "Height": []})

# ファイルごと（フレームごと）に操作
for num, file in enumerate(files):
    with open(file) as open_file:
        json_data = json.load(open_file)

        # 動的特徴量（各相対距離）を算出
        dx1 = abs(json_data["10"][0] - json_data["13"][0])
        dx2 = abs(json_data["6"][0] - json_data["3"][0])
        dx3 = abs(json_data["7"][0] - json_data["4"][0])
        dx4 = abs(json_data["0"][0] - (json_data["13"][0] + json_data["10"][0]) / 2)
        dx5 = abs((json_data["8"][0] + json_data["11"][0]) / 2 - (json_data["13"][0] + json_data["10"][0]) / 2)
        dx6 = abs(json_data["5"][0] - json_data["2"][0])
        dy1 = abs(json_data["0"][1] - (json_data["13"][1] + json_data["10"][1]) / 2)
        dy2 = abs(json_data["0"][1] - (json_data["12"][1] + json_data["9"][1]) / 2)
        dy3 = abs(json_data["10"][1] - json_data["13"][1])

        # 静的特徴を算出
        dis0_1 = get_distance(json_data["0"][0], json_data["0"][1], json_data["1"][0], json_data["1"][1])
        # dis1_2 = get_distance(json_data["2"][0], json_data["2"][1], json_data["3"][0], json_data["3"][1]) #横から撮影のため削除
        dis2_3 = get_distance(json_data["2"][0], json_data["2"][1], json_data["3"][0], json_data["3"][1])
        dis3_4 = get_distance(json_data["3"][0], json_data["3"][1], json_data["4"][0], json_data["4"][1])
        dis1_8 = get_distance(json_data["1"][0], json_data["1"][1], json_data["8"][0], json_data["8"][1])
        dis8_9 = get_distance(json_data["8"][0], json_data["8"][1], json_data["9"][0], json_data["9"][1])
        dis9_10 = get_distance(json_data["9"][0], json_data["9"][1], json_data["10"][0], json_data["10"][1])
        dis1_11 = get_distance(json_data["1"][0], json_data["1"][1], json_data["11"][0], json_data["11"][1])
        dis11_12 = get_distance(json_data["11"][0], json_data["11"][1], json_data["12"][0], json_data["12"][1])
        dis12_13 = get_distance(json_data["12"][0], json_data["12"][1], json_data["13"][0], json_data["13"][1])
        # dis0_5 = get_distance(json_data["2"][0], json_data["2"][1], json_data["3"][0], json_data["3"][1]) #横から撮影のため削除
        dis5_6 = get_distance(json_data["5"][0], json_data["5"][1], json_data["6"][0], json_data["6"][1])
        dis6_7 = get_distance(json_data["6"][0], json_data["6"][1], json_data["7"][0], json_data["7"][1])
        dis1_8and11 = (dis1_8 + dis1_11) / 2

        # 骨格の長さ身長
        skeleton_len = dis0_1 + dis2_3 + dis3_4 + dis1_8 + dis8_9 + dis9_10 + dis1_11 + dis11_12 + dis12_13
        height = dis0_1 + dis1_8and11 + ((dis8_9 + dis9_10 + dis11_12 + dis12_13) / 2)

        # 特徴空間を作成
        feature_df.loc[str(num)] = {"Dx1": dx1,
                                    "Dx2": dx2,
                                    "Dx3": dx3,
                                    "Dx4": dx4,
                                    "Dx5": dx5,
                                    "Dx6": dx6,
                                    "Dy1": dy1,
                                    "Dy2": dy2,
                                    "Dy3": dy3,
                                    "Dis0_1": dis0_1,
                                    "Dis2_3": dis2_3,
                                    "Dis3_4": dis3_4,
                                    "Dis1_8": dis1_8,
                                    "Dis8_9": dis8_9,
                                    "Dis9_10": dis9_10,
                                    "Dis1_11": dis1_11,
                                    "Dis11_12": dis11_12,
                                    "Dis12_13": dis12_13,
                                    "Dis5_6": dis5_6,
                                    "Dis6_7": dis6_7,
                                    "Dis1_8and11": dis1_8and11,
                                    "Height": height
                                    }
    if num == 10:
        break

# print(feature_df)

# 特徴空間の平均、標準偏差を算出（rdf）
mean_feature_names = ["mDx1", "mDx2", "mDx3", "mDx4", "mDx5", "mDx6",
                      "mDy1", "mDy2", "mDy3",
                      "Dis0_1", "Dis2_3", "Dis3_4", "Dis1_8", "Dis8_9", "Dis9_10",
                      "Dis1_11", "Dis11_12", "Dis12_13", "Dis5_6", "Dis6_7", "Dis1_8and11",
                      "Height"]
mean_val_list = list(pd.DataFrame.mean(feature_df))
MEAN = pd.DataFrame([mean_val_list], columns=mean_feature_names)

std_feature_names = ["stDx1", "stDx2", "stDx3", "stDx4", "stDx5", "stDx6",
                     "stDy1", "stDy2", "stDy3"]
std_val_list = list(pd.DataFrame.std(feature_df))
STD = pd.DataFrame([std_val_list[:-13]], columns=std_feature_names)

CF = pd.concat([MEAN, STD], axis=1)
print(CF)

# データの上書き、新規作成
path = './feature_sets/feature_1.json'
CF.to_json(path)
