import json
import glob
import sys
import numpy as np
import collections as cl
from pprint import pprint
from natsort import natsorted

files = natsorted(glob.glob("./json_new/*"))
joint_list = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
              "10", "11", "12", "13", "14", "15", "16", "17"]
only_c_data = {'0': [], "1": [], "2": [], "3": [], "4": [], "5": [],
               "6": [], "7": [], "8": [], "9": [], "10": [], "11": [],
               "12": [], "13": [], "14": [], "15": [], "16": [], "17": []}

for file in files:
    with open(file) as open_file:
        coordinates_data = json.load(open_file)
        for i in range(len(coordinates_data)):
            only_c_data[joint_list[i]].append(coordinates_data[joint_list[i]][2])

for i in range(len(joint_list)):
    coordinates_mean = np.mean(only_c_data[joint_list[i]])
    coordinates_std = np.std(only_c_data[joint_list[i]])
    print("joint = " + joint_list[i])
    print("c_mean", coordinates_mean)
    print("c_std", coordinates_std)
    print()
