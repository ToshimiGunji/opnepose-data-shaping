import json
from pprint import pprint
import sys
import glob
import collections as cl


def main():
    files = glob.glob("./json/*")
    joint_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17"]
    file = "./json_sub/wakingVideoLowQ_000000000000_keypoints.json"
    cl_data = cl.OrderedDict()

    with open(file) as open_file:
        json_data = json.load(open_file)
        part_candidates_data = json_data["part_candidates"][0]  # ジョイントデータにアクセスするために前部分を省略

        for i in range(len(part_candidates_data)):  # 座標のリスト数分だけ回す
            confidence_data = []  # confidenceを格納するリスト。座標のリストごとに更新する
            for j in range(int(len(part_candidates_data[joint_list[i]]) / 3)):  # confidenceの数だけ繰り返す
                confidence_data_pos = (j + 1) * 3 - 1  # 信頼度データの場所
                confidence_data.append(part_candidates_data[joint_list[i]][confidence_data_pos])

            confidence_index = confidence_data.index(max(confidence_data))
            for j in range(len(part_candidates_data)):  # 座標のリスト数分だけ回す
                print()

            print(joint_list[i] + "joint")
            print(confidence_data)
            print(confidence_index)

        # データの上書き、新規作成
        fw = open('./json_new/new.json', 'w')
        json.dump(cl_data, fw, indent=4)

    # # 全ファイルの内容を出力
    # for file in files:
    #     print(file)
    #     with open(file) as open_file:
    #         json_data = json.load(open_file)
    #         for joint in joint_list:
    #             pprint("{0}  :{1}".format(joint, json_data["part_candidates"][0][joint]))


if __name__ == "__main__":
    main()
