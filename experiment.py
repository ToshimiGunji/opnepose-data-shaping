import json
import glob
import collections as cl
import sys
from pprint import pprint
from natsort import natsorted
import pandas as pd
import numpy as np
from numpy import nan

# pd.set_option('display.max_columns', 100)

file = "./json_new/new_137.json"
with open(file) as open_file:
    json_data = json.load(open_file)
    df_j = pd.DataFrame(json_data)

print(df_j)
pprint(json_data)
print(type(json_data))
