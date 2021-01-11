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

feature_df = pd.DataFrame({"Dx1": [], "Dx2": [], "Dx3": [], "Dx4": [], "Dx5": [], "Dx6": [],
                           "Dy1": [], "Dy2": [], "Dy3": [],
                           "SkeletonLength": [], "Height": []})

files = natsorted(glob.glob("./json_new/*"))

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
                                    "SkeletonLength": skeleton_len,
                                    "Height": height
                                    }
    pprint(feature_df)
    if num == 5:
        break

# 特徴空間の平均、標準偏差を算出（rdf）
rdf = pd.DataFrame({"Dx1": [], "Dx2": [], "Dx3": [], "Dx4": [], "Dx5": [], "Dx6": [],
                    "Dy1": [], "Dy2": [], "Dy3": [],
                    "SkeletonLength": [], "Height": []
                    })
