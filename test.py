import sys
import json
import pprint
import numpy

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
print("HAND LEFT")
print(hand_left)
print("HAND_RIGHT")
print(hand_right)