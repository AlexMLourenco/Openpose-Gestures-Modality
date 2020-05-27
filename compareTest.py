import sys
import json
import pprint
from dtaidistance import dtw
from dtaidistance import dtw_visualisation as dtwvis
import numpy as np
from os import listdir
from os.path import isfile, join
from test import get_distances, get_keypoints

#---------------------Euclidian--------------------------------#
def get_euclidian(points):
    
    fk = {}
    for keypoint in range(len(points)):  
        for frame in points[keypoint]:
            d0 = []
            for key in range(len(points[keypoint][frame]["x"])):
                f0k0 = [points[keypoint][frame]["x"][key], points[keypoint][frame]["y"][key]]
                d0.append(f0k0)
                #print(frame)
                fk[frame] = d0
                
    print(fk)
    print(len(d0))
#--------------------------- MAIN-------------------------------------#
file_name = "./json/" + sys.argv[1] + ".json"
mypath = "./json/"

onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
onlyfiles.remove(sys.argv[1]+".json")

hand_right = []
x = []
y = []

with open(file_name) as json_file:
    data = json.load(json_file)

    for key in data["data"]:
        hand_right.append(data["data"][key][0]["hand_left_keypoints_2d"])

    keypoints_right_1 = get_keypoints(hand_right)

    get_euclidian(keypoints_right_1)

    #print(keypoints_right_1)
     
for f in onlyfiles:
    with open("./json/"+f) as json_file:
        data = json.load(json_file)

        hand_right = []
        for key in data["data"]:
            hand_right.append(data["data"][key][0]["hand_left_keypoints_2d"])
            label = data["label"]
            identifier = data["id"]

        keypoints_right_2 = get_keypoints(hand_right)
        #print(label)
        #print(identifier)

        dist_right = get_distances(keypoints_right_1,keypoints_right_2)
        #print(dist_right)