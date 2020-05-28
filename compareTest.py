import sys
import json
import pprint
from dtaidistance import dtw
from dtaidistance import dtw_visualisation as dtwvis
from scipy.spatial.distance import euclidean
from fastdtw import fastdtw
import numpy as np
from os import listdir
from os.path import isfile, join
from test import get_distances, get_keypoints

#---------------------Euclidian--------------------------------#
def get_euclidian(points,points2,id):
    
    fk = {}
    for keypoint in range(len(points)):  
        for frame in points[keypoint]:
            d0 = []
            for key in range(len(points[keypoint][frame]["x"])):
                if(points[keypoint][frame]["x"][key] != 0 or points[keypoint][frame]["x"][key] != 0):
                    f0k0 = [points[keypoint][frame]["x"][key], points[keypoint][frame]["y"][key]]
                    d0.append(f0k0)
                    fk[frame] = d0

    fk2 = {}
    for keypoint in range(len(points2)):  
        for frame in points2[keypoint]:
            d0 = []
            for key in range(len(points2[keypoint][frame]["x"])):
                if(points2[keypoint][frame]["x"][key] != 0 or points2[keypoint][frame]["x"][key] != 0):
                    f0k0 = [points2[keypoint][frame]["x"][key], points2[keypoint][frame]["y"][key]]
                    d0.append(f0k0)
            fk2[frame] = d0
                
    dist = {label: 0}
    distan = 0
    for key in range(len(fk)):
        x = fk[key]
        #print(x)
        y = fk2[key]
        distance, path = fastdtw(x,y, dist=euclidean)
        distan += distance
        
    dist[label] = distan/20
    #distance, path = fastdtw(x, y, dist=euclidian)
    #print(distance)
    return distan/20
    #print("primeiro:" + str(fk))
    #print("segundo:" + str(fk2))
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
        hand_right.append(data["data"][key][0]["hand_right_keypoints_2d"])

    keypoints_right_1 = get_keypoints(hand_right)

    
    #print(keypoints_right_1)
d = {}
di = []
for f in onlyfiles:
    with open("./json/"+f) as json_file:
        data = json.load(json_file)

        hand_right = []
        for key in data["data"]:
            label = data["label"]
            identifier = data["id"]
            
            print(data["data"][key][0]["hand_right_keypoints_2d"])
            hand_right.append(data["data"][key][0]["hand_right_keypoints_2d"])
            
        di.append({"label": label, "identifier": identifier})
        keypoints_right_2 = get_keypoints(hand_right)
       
        print(identifier + "\n")
        print(label + "\n")
        dist_right = get_distances(keypoints_right_1,keypoints_right_2)
        #print(dist_right)
    
    dist = get_euclidian(keypoints_right_1,keypoints_right_2,identifier)
    if dist > 0:
        d[identifier] = dist

print(d)
a = []

key_list = list(d.keys()) 
val_list = list(d.values()) 
    
#print(key_list[val_list.index(min(val_list))]) 
for item in di:
    if item["identifier"] == key_list[val_list.index(min(val_list))]:
        print("O gesto que tem menor distancia é: " + item["label"])
        break


    