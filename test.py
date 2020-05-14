import sys
import json
import pprint
from dtaidistance import dtw
from dtaidistance import dtw_visualisation as dtwvis
import numpy as np


#------------------------ Keypoints variation (x , y) --------------------""
def get_keypoints(_array):

    keypoints_pose = list({i:{"x":[],"y":[]}} for i in range(len(_array[0])//3))
    for item in _array:
        for k in range(len(keypoints_pose)):
            j = k*3 + 1
            keypoints_pose[k][k]["x"].append(item[k*3])
            keypoints_pose[k][k]["y"].append(item[j])
    return keypoints_pose
#-------------- Calc distances -------------------------------------#
def get_distances(keypoints1, keypoints2):

    distances = list({i:{"dist_x":[],"dist_y":[]}} for i in range(len(keypoints1)))

    for i in range(len(distances)):
        distances[i][i]["dist_x"].append(dtw.distance(keypoints1[i][i]["x"], keypoints2[i][i]["x"])) 
        distances[i][i]["dist_y"].append(dtw.distance(keypoints1[i][i]["y"], keypoints2[i][i]["y"]))

    return distances


#--------------------------- MAIN-------------------------------------#


file_name = ".\\json\\" + sys.argv[1]
file2_name = ".\\json\\" + sys.argv[2]

pose_arr = []
hand_left = []
hand_right = []
pose_arr2 = []
hand_left2 = []
hand_right2 = []




with open(file_name) as json_file:
    data = json.load(json_file)

    for key in data["data"]:
        pose_arr.append(data["data"][key][0]["pose_keypoints_2d"])
        hand_left.append(data["data"][key][0]["hand_left_keypoints_2d"])
        hand_right.append(data["data"][key][0]["hand_right_keypoints_2d"])

with open(file2_name) as json_file:
    data = json.load(json_file)

    for key in data["data"]:
        pose_arr2.append(data["data"][key][0]["pose_keypoints_2d"])
        hand_left2.append(data["data"][key][0]["hand_left_keypoints_2d"])
        hand_right2.append(data["data"][key][0]["hand_right_keypoints_2d"])

 
    
    keypoints_pose_1 = get_keypoints(pose_arr)
    keypoints_pose_2 = get_keypoints(pose_arr2)
    #keypoints_left_hand = get_keypoints(hand_left)
    #keypoints_right_hand = get_keypoints(hand_right)
    dist = get_distances(keypoints_pose_1,keypoints_pose_2)
    print(dist)
