import sys
import json
import pprint
from dtaidistance import dtw
from dtaidistance import dtw_visualisation as dtwvis
import numpy as np

file_name = ".\\json\\" + sys.argv[1]

pose_arr = []
hand_left = []
hand_right = []

with open(file_name) as json_file:
    data = json.load(json_file)

    for key in data["data"]:
        pose_arr.append(data["data"][key][0]["pose_keypoints_2d"])
        hand_left.append(data["data"][key][0]["hand_left_keypoints_2d"])
        hand_right.append(data["data"][key][0]["hand_right_keypoints_2d"])

    print("POSE ARRAY")
    print(pose_arr)
    keypoint1_x = [i[0] for i in pose_arr]
    keypoint1_y = [i[1] for i in pose_arr]

print(keypoint1_y)
print(keypoint1_x)
# path = dtw.warping_path(s1, s2)
# dtwvis.plot_warping(s1, s2, path, filename="warp.png")
# s1 = [0, 0, 1, 2, 1, 0, 1, 0, 0]
# s2 = [0, 1, 2, 0, 0, 0, 0, 0, 0]
dist = dtw.distance(keypoint1_x, keypoint1_x)
print(dist)
# print("HAND LEFT")
# print(hand_left)
# print("HAND_RIGHT")
# print(hand_right)