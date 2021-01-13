import json
import glob
import collections as cl
import sys
from pprint import pprint
from natsort import natsorted
from numpy import nan


def data_wrangle(person_num, gl_pr, down_up, gl_pr_set):
    files = natsorted(glob.glob("./json/raw/{0}/{1}/{2}/{3}/*".format(person_num, gl_pr, down_up, gl_pr_set)))
    for num, file in enumerate(files):
        with open(file) as open_file:
            json_data = json.load(open_file)
            shaped_data = cl.OrderedDict()  # いらない要素を削除した後の数値を格納するリスト。順番を維持したCollection型
            part_candidates_data = json_data["part_candidates"][0]  # ジョイントデータにアクセスするために前部分を省略

            # 信頼度の高いデータ以外を削除
            for i in range(len(part_candidates_data)):  # 関節のリスト数分だけ回す （18回）
                confidence_data = []  # confidenceを格納するリスト。座標のリストごとに更新する

                # 信頼度のデータだけを格納
                for j in range(int(len(part_candidates_data[joint_list[i]]) / 3)):  # confidenceの数だけ繰り返す
                    c_data_pos = (j + 1) * 3 - 1  # 信頼度データの場所
                    confidence_data.append(part_candidates_data[joint_list[i]][c_data_pos])

                # max関数のエラー回避のためにconfidence_dataが空の場合はスキップ。信頼度の最大値インデックスを返す
                if len(confidence_data) == 0:
                    confidence_index = 0  # エラー回避のために代入
                    part_candidates_data[joint_list[i]] = [nan, nan, nan]  # 各要素に0を代入
                    # print(i)
                else:
                    confidence_index = confidence_data.index(max(confidence_data))  # 信頼度の最大値インデックスを返す

                # 信頼度の低い要素を削除
                for j in range(len(part_candidates_data[joint_list[i]])):  # 座標のリスト数分だけ回す
                    if j == confidence_index * 3 \
                            or j == confidence_index * 3 + 1 \
                            or j == confidence_index * 3 + 2:
                        pass
                    else:
                        part_candidates_data[joint_list[i]][j] = ""  # いらないデータに空データを代入

                    shaped_data[joint_list[i]] = [datum for datum in part_candidates_data[joint_list[i]]
                                                  if datum != ""]  # 空の要素以外を格納する

            # データの上書き、新規作成
            target_path = "./json/shaped/{0}/{1}/{2}/{3}/shaped_{4}.json" \
                .format(person_num, gl_pr, down_up, gl_pr_set, num)
            fw = open(target_path, 'w')
            json.dump(shaped_data, fw, indent=4)


joint_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
              "10", "11", "12", "13", "14", "15", "16", "17"]
person_num = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]
gl_pr = ["gallery", "probe"]
down_up = ["down", "up"]
gl_set = ["0", "1", "2"]
pr_set = ["0"]

for person in person_num:
    for g_p in gl_pr:
        for d_u in down_up:
            if g_p == "gallery":  # ギャラリーデータセットへアクセス
                for gl in gl_set:
                    data_wrangle(person, g_p, d_u, gl)
            if g_p == "probe":  # プローブデータセットへアクセス
                for pr in pr_set:
                    data_wrangle(person, g_p, d_u, pr)
    if person == 1:
        break
