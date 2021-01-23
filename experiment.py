import json
import glob
import collections as cl
import sys
from pprint import pprint
from natsort import natsorted
import pandas as pd
from numpy import array
from numpy import nan
import os
import statistics
# pd.set_option('display.max_columns', 100)
import random
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris
from sklearn.neighbors import KNeighborsClassifier
import matplotlib as mpl
import matplotlib.pyplot as plt

k = [1, 3, 5, 7, 9, 11]
accuracy_rdf = [
    [50.0, 41.66666666666667, 66.66666666666666, 33.33333333333333, 33.33333333333333, 33.33333333333333],
    [58.333333333333336, 50.0, 50.0, 50.0, 33.33333333333333, 33.33333333333333],
    [58.333333333333336, 33.33333333333333, 50.0, 33.33333333333333, 33.33333333333333, 33.33333333333333],
    [50.0, 50.0, 58.333333333333336, 41.66666666666667, 33.33333333333333, 33.33333333333333],
    [58.333333333333336, 41.66666666666667, 50.0, 33.33333333333333, 33.33333333333333, 33.33333333333333]
]
accuracy_af = [
    [75.0, 83.33333333333334, 66.66666666666666, 41.66666666666667, 33.33333333333333, 25.0],
    [75.0, 83.33333333333334, 50.0, 41.66666666666667, 33.33333333333333, 25.0],
    [83.33333333333334, 83.33333333333334, 66.66666666666666, 41.66666666666667, 33.33333333333333, 25.0],
    [75.0, 83.33333333333334, 58.333333333333336, 41.66666666666667, 33.33333333333333, 25.0],
    [75.0, 83.33333333333334, 58.333333333333336, 41.66666666666667, 33.33333333333333, 25.0]
]

accuracy_cf = [
    [75.0, 75.0, 58.333333333333336, 41.66666666666667, 25.0, 33.33333333333333],
    [75.0, 58.333333333333336, 50.0, 41.66666666666667, 33.33333333333333, 25.0],
    [75.0, 41.66666666666667, 58.333333333333336, 41.66666666666667, 25.0, 33.33333333333333],
    [75.0, 66.66666666666666, 66.66666666666666, 33.33333333333333, 33.33333333333333, 25.0],
    [75.0, 58.333333333333336, 58.333333333333336, 41.66666666666667, 25.0, 25.0]
]

accuracy_rdf_mean = array(accuracy_rdf).mean(axis=0)
accuracy_af_mean = array(accuracy_af).mean(axis=0)
accuracy_cf_mean = array(accuracy_cf).mean(axis=0)

plt.figure()
plt.plot(k, accuracy_rdf_mean, marker="D")
plt.plot(k, accuracy_af_mean, marker="^")
plt.plot(k, accuracy_cf_mean, marker="o")

plt.title("accuracy / k")
plt.xlabel("k value")
plt.ylabel("accuracy (%)")
plt.title("accuracy / k", fontsize=14)
plt.xlabel("k value", fontsize=14)
plt.ylabel("accuracy (%)", fontsize=14)
plt.legend(fontsize=14)

plt.grid(True)
plt.xticks([1, 3, 5, 7, 9, 11])
plt.yticks([20, 40, 60, 80, 100])
plt.legend(["RDF", "AF", "CF"])
plt.show()
