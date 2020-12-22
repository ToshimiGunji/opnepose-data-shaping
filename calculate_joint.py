import json
import glob
import collections as cl
from pprint import pprint
from natsort import natsorted

files = natsorted(glob.glob("./json_new/*"))
joint_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
              "10", "11", "12", "13", "14", "15", "16", "17"]

pprint(files)
for num, file in enumerate(files):
    with open(file) as open_file:
        json_data = json.load(open_file)
        part_candidates_data = json_data["part_candidates"][0]  # ジョイントデータにアクセスするために前部分を省略
