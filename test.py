import sys
import json
import pprint
from dtaidistance import dtw
from dtaidistance import dtw_visualisation as dtwvis
import numpy as np
from scipy.spatial.distance import euclidean

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
'''
file_name = ".\\json\\" + sys.argv[1] + ".json"
file2_name = ".\\json\\" + sys.argv[2] + ".json"

pose_arr = []
hand_left = []
hand_right = []
pose_arr2 = []
hand_left2 = []
hand_right2 = []

x = []
y = []

x1 = []
x2 = []

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
    
    #keypoints_pose_1 = get_keypoints(pose_arr)
    #keypoints_pose_2 = get_keypoints(pose_arr2)
    keypoints_right_1 = get_keypoints(hand_right)
    keypoints_right_2 = get_keypoints(hand_right2)

    keypoints_left_1 = get_keypoints(hand_left)
    keypoints_left_2 = get_keypoints(hand_left2)

    print("|-----------------------------------------------------------------------------------------|")
    print("|------------------------------LEFT HAND KEY POINTS---------------------------------------|")
    print("|-----------------------------------------------------------------------------------------|")
    print(keypoints_left_1)
    print("|-----------------------------------------------------------------------------------------|")
    print("|------------------------------RIGHT HAND KEY POINTS--------------------------------------|")
    print("|-----------------------------------------------------------------------------------------|")
    print(keypoints_right_1)

    dist_right = get_distances(keypoints_right_1,keypoints_right_2)
    dist_left = get_distances(keypoints_left_1,keypoints_left_2)
    
    print("|-----------------------------------------------------------------------------------------|")
    print("|----------------------------------RIGHT HAND---------------------------------------------|")
    print("|-----------------------------------------------------------------------------------------|")
    print(dist_right)
    print("|-------------------------------RIGHT X HAND VAR------------------------------------------|")

    for index in range(len(dist_right)):
        for key in dist_right[index]:
            x.append(dist_right[index][key]["dist_x"])
            y.append(dist_right[index][key]["dist_y"])

    print(np.var(x, axis=0))

    print("|-------------------------------RIGHT X HAND VAR------------------------------------------|")

    print(np.var(y, axis=0))

    print("|---------------------------------RIGHT X HAND STD----------------------------------------|")
    print(np.std(x, dtype=np.float64))

    print("|---------------------------------RIGHT Y HAND STD----------------------------------------|")
    print(np.std(y, dtype=np.float64))
    
    print("|-----------------------------------------------------------------------------------------|")
    print("|-----------------------------------LEFT HAND---------------------------------------------|")
    print("|-----------------------------------------------------------------------------------------|")
    print(dist_left)

    for index in range(len(keypoints_right_1)):
        for key in keypoints_right_1[index]:
            x1.append(keypoints_right_1[index][key]["x"])
            
    for index in range(len(keypoints_right_2)):
        for key in keypoints_right_2[index]:
            x2.append(keypoints_right_2[index][key]["x"])

    name = ".\\warps\\" + "warp"+sys.argv[1]+"&"+sys.argv[2]+".png"

    path = dtw.warping_path(np.array(x1[5]), np.array(x2[5]))
    dtwvis.plot_warping(np.array(x1[5]), np.array(x2[5]), path, filename=name)
'''