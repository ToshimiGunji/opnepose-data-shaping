import json
import glob
from natsort import natsorted
import pandas as pd
from numpy import abs
from math import sqrt
import sys
from numpy import nan
import numpy as np
from pprint import pprint

pd.set_option('display.max_columns', 100)


# 座標から距離を算出
def get_distance(x1, y1, x2, y2):
    dis = sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return dis


def get_cf(person_num, gl_pr, down_up, gl_pr_set):
    files = natsorted(glob.glob("./json/shaped/{0}/{1}/{2}/{3}/*".format(person_num, gl_pr, down_up, gl_pr_set)))
    # 一時的に格納するデータフレーム
    feature_df = pd.DataFrame({"Dx1": [], "Dx2": [], "Dx3": [], "Dx4": [], "Dx5": [], "Dx6": [],
                               "Dy1": [], "Dy2": [], "Dy3": [],
                               "Dis0_1": [], "Dis2_3": [], "Dis3_4": [], "Dis1_8": [], "Dis8_9": [], "Dis9_10": [],
                               "Dis1_11": [], "Dis11_12": [], "Dis12_13": [], "Dis5_6": [], "Dis6_7": [],
                               "Dis1_8and11": [],
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
            # 横から撮影のため削除
            # dis1_2 = get_distance(json_data["2"][0], json_data["2"][1], json_data["3"][0], json_data["3"][1])
            dis2_3 = get_distance(json_data["2"][0], json_data["2"][1], json_data["3"][0], json_data["3"][1])
            dis3_4 = get_distance(json_data["3"][0], json_data["3"][1], json_data["4"][0], json_data["4"][1])
            dis1_8 = get_distance(json_data["1"][0], json_data["1"][1], json_data["8"][0], json_data["8"][1])
            dis8_9 = get_distance(json_data["8"][0], json_data["8"][1], json_data["9"][0], json_data["9"][1])
            dis9_10 = get_distance(json_data["9"][0], json_data["9"][1], json_data["10"][0], json_data["10"][1])
            dis1_11 = get_distance(json_data["1"][0], json_data["1"][1], json_data["11"][0], json_data["11"][1])
            dis11_12 = get_distance(json_data["11"][0], json_data["11"][1], json_data["12"][0], json_data["12"][1])
            dis12_13 = get_distance(json_data["12"][0], json_data["12"][1], json_data["13"][0], json_data["13"][1])
            # 横から撮影のため削除
            # dis0_5 = get_distance(json_data["2"][0], json_data["2"][1], json_data["3"][0], json_data["3"][1])
            dis5_6 = get_distance(json_data["5"][0], json_data["5"][1], json_data["6"][0], json_data["6"][1])
            dis6_7 = get_distance(json_data["6"][0], json_data["6"][1], json_data["7"][0], json_data["7"][1])
            dis1_8and11 = (dis1_8 + dis1_11) / 2
            # 身長
            height = dis0_1 + dis1_8and11 + ((dis8_9 + dis9_10 + dis11_12 + dis12_13) / 2)
            # 一時的な特徴空間を作成
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

    # 平均値特徴名リスト
    mean_feature_names = ["mDx1", "mDx2", "mDx3", "mDx4", "mDx5", "mDx6",
                          "mDy1", "mDy2", "mDy3",
                          "Dis0_1", "Dis2_3", "Dis3_4", "Dis1_8", "Dis8_9", "Dis9_10",
                          "Dis1_11", "Dis11_12", "Dis12_13", "Dis5_6", "Dis6_7", "Dis1_8and11",
                          "Height"]
    # 標準偏差特徴名リスト
    std_feature_names = ["stDx1", "stDx2", "stDx3", "stDx4", "stDx5", "stDx6",
                         "stDy1", "stDy2", "stDy3"]
    # 平均値
    mean_val_list = list(pd.DataFrame.mean(feature_df))
    mean_df = pd.DataFrame([mean_val_list], columns=mean_feature_names)
    # 標準偏差
    std_val_list = list(pd.DataFrame.std(feature_df))
    std_df = pd.DataFrame([std_val_list[:-13]], columns=std_feature_names)
    # 平均と標準偏差を結合
    if down_up == "down":
        cf = pd.concat([std_df, mean_df], axis=1)
    if down_up == "up":
        dropped_mean = mean_df.drop(mean_df.columns[-13:], axis=1)  # upのときは静的特徴を削除
        cf = pd.concat([std_df, dropped_mean], axis=1)
        cf.columns = ["u_stDx1", "u_stDx2", "u_stDx3", "u_stDx4", "u_stDx5", "u_stDx6", "u_stDy1", "u_stDy2", "u_stDy3",
                      "u_mDx1", "u_mDx2", "u_mDx3", "u_mDx4", "u_mDx5", "u_mDx6", "u_mDy1", "u_mDy2", "u_mDy3"]
    return cf


# 全ファイルにアクセスして特徴量を抽出
person_num = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]
gl_pr = ["gallery", "probe"]
down_up = ["down", "up"]
gl_set = ["0", "1", "2"]
pr_set = ["0"]

for person in person_num:
    for g_p in gl_pr:
        cf_gl_down_list = []  # cf のdownを一時的に格納
        cf_gl_up_list = []  # cf のupを一時的に格納
        cf_pr_down_list = []  # cf のdownを一時的に格納
        cf_pr_up_list = []  # cf のupを一時的に格納
        for d_u in down_up:
            if g_p == "gallery":  # ギャラリーデータセットへアクセス
                for gl in gl_set:
                    cf_gl = get_cf(person, g_p, d_u, gl)
                    cf_gl_down_list.append(cf_gl) if d_u == "down" else cf_gl_up_list.append(cf_gl)
            if g_p == "probe":  # プローブデータセットへアクセス
                for pr in pr_set:
                    cf_pr = get_cf(person, g_p, d_u, pr)
                    cf_pr_down_list.append(cf_pr) if d_u == "down" else cf_pr_up_list.append(cf_pr)
        # ギャラリーとプローブ特徴量をjsonに変換し保存
        if g_p == "gallery":
            for num, (d_data, u_data) in enumerate(zip(cf_gl_down_list, cf_gl_up_list)):
                all_CF = pd.concat([d_data, u_data], axis=1)
                # データの上書き、新規作成
                target_path = './json/feature_sets/{0}/{1}/feature_{2}.json'.format(person, g_p, num)
                all_CF.to_json(target_path)
                print(target_path)
        else:
            for num, (d_data, u_data) in enumerate(zip(cf_pr_down_list, cf_pr_up_list)):
                all_CF = pd.concat([d_data, u_data], axis=1)
                # データの上書き、新規作成
                target_path = './json/feature_sets/{0}/{1}/feature_{2}.json'.format(person, g_p, num)
                all_CF.to_json(target_path)
                print(target_path)
