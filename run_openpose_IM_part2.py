import argparse
import datetime
import json
import os
import shutil
import subprocess
import sys
from os.path import isdir, isfile, join

import numpy as np
import pandas as pd
from tqdm import tqdm

from scripts.format_json import json_join

OPEN_POSE_DIR = "C:\\Users\\manel\\Desktop\\openpose-1.5.1-binaries-win64-gpu-python-flir-3d_recommended\\openpose"

def get_now():
    return datetime.datetime.now().strftime('%y-%m-%d_%H%M%S')


def write_log(log_name, message, log_type='INFO'):
    with open(log_name, 'a') as f:
        f.write('[{0}] [{2}]: {1}\n'.format(get_now(), message, log_type))


def shutdown(message='Shutting down machine'):
    print("Shutting down... " + str(message))
    sys.exit(0)
    # os.system('shutdown now')



vid_dir = 'videos' # [IM 23-04] originally 20bn-datasets/20bn-jester-v1
json_dir = 'json'
log_dir = 'logs'

label_dir = 'labels'
script_dir = 'scripts'


# The the absolute directory path of where the python file is located
root = os.path.dirname(os.path.realpath(__file__))

# Change the relative paths to absolute paths
vid_dir = join(root, vid_dir)
if not os.path.isdir(vid_dir): 
    os.mkdir(vid_dir)

json_dir = join(root, json_dir)
if not os.path.isdir(json_dir): 
    os.mkdir(json_dir)

log_dir = join(root, log_dir)
if not os.path.isdir(log_dir): 
    os.mkdir(log_dir)

label_dir = join(root, label_dir)
if not os.path.isdir(label_dir): 
    os.mkdir(label_dir)

script_dir = join(root, script_dir)
if not os.path.isdir(script_dir): 
    os.mkdir(script_dir)

try:
    now = get_now()
    log = join(log_dir, now + '.txt')
    write_log(log, 'Starting logging for execution in time {}'.format(now))

except BaseException as e:
    shutdown(e)


try:
    write_log(log, 'Getting labels', log_type='INFO')
    json_file = join(label_dir, 'train.csv')
    labels = pd.read_csv(json_file, index_col=0, sep=';', header=None)
    labels = json.loads(labels.to_json())['1']

    json_file = join(label_dir, 'validation.csv')
    validation_labels = pd.read_csv(
        json_file, index_col=0, sep=';', header=None)
    validation_labels = json.loads(validation_labels.to_json())['1']

    json_file = join(label_dir, 'test.csv')
    test_labels = pd.read_csv(json_file, index_col=0, sep=';', header=None)
    test_labels['1'] = '?'
    test_labels = json.loads(test_labels.to_json())['1']

    labels.update(validation_labels)
    labels.update(test_labels)
    write_log(log, 'Labels Updated', log_type='INFO')

except BaseException as e:
    write_log(log, 'Unable to get labels: {}'.format(e), log_type='FATAL')
    shutdown(e)


# Get the video directories only as directory name
try:
    write_log(log, 'Getting video lists', log_type='INFO')
    vid_list = [i for i in os.listdir(vid_dir) if isdir(join(vid_dir, i))]
    vid_list = np.random.permutation(vid_list)
    write_log(log, 'Done getting video lists: {}'.format(vid_list), log_type='INFO')
except BaseException as e:
    write_log(log, 'Cannot get video lists', log_type='FATAL')
    shutdown(e)


for i in tqdm(vid_list):
    write_log(log, 'Run OpenPose', log_type='INFO')
    input_dir = join(vid_dir, i)
    output_dir = join(json_dir, i)
    big_json_name = output_dir + '.json'
    write_log(log, '-' * 64)
    write_log(log, 'Starting video {}'.format(i))

    # if the directory exists then we can skip it
    # In case we run need to run it twice.
    try:
        if isfile(big_json_name):
            write_log(log, 'Big json exists going to next video')
            continue
        else:
            write_log(log, 'Making json directory')
            os.makedirs(output_dir)

    except BaseException as e:
        write_log(
            log, 'Something wrong with json file/dir: {}'.format(e), log_type='ERROR')
        #continue

    ### run the openpose command ###
   # write_log(log, 'Extracting features using openPose')
   # if (os.name == "nt"):
   #     write_log(log, 'Windows version')
   #     rc = subprocess.run(['.\\scripts\\openpose.bat', '{}'.format(OPEN_POSE_DIR), '{}'.format(input_dir),
   #                         '{}'.format(output_dir)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   # else:
   #     #rc = subprocess.run(['./scripts/openpose.sh', '{}'.format(input_dir),
   #     #                     '{}'.format(output_dir)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   #     print()

   # if rc.returncode == 0:
   #     write_log(log, rc.stdout)
   #     write_log(log, 'Features extracted for video {}'.format(
   #         i), log_type='COMPL')
   # else:
   #     write_log(log, 'Unable to complete openPose extraction',
   #               log_type='ERROR')
   #     write_log(log, 'Openpose stdout: {}'.format(str(rc.stdout)))
   #     write_log(log, 'OpenPose stderr: {}'.format(str(rc.stderr)))
   #     write_log(log, 'Delete json directory of {}'.format(i))
   #     shutil.rmtree(output_dir)
   #     continue

    ### Combine the json scripts into one ###
    print (labels)

    try:
        big_json = json_join(output_dir, labels)
        with open(big_json_name, 'w') as j:
            json.dump(big_json, j)
        write_log(log, 'Concatenating json files')
        print ('Concatenating  json files')
    except BaseException as e:
        if isfile(big_json_name):
            os.remove(big_json_name)
        write_log(log, 'Concat json files {}'.format(e), log_type='ERROR')
        print('Concat json files {}'.format(e))
        continue

    try:
        if isfile(big_json_name):
            write_log(log, 'Removing json dir')
            shutil.rmtree(output_dir)
        else:
            write_log(log, 'No file names {}'.format(
                big_json_name), log_type='ERROR')
    except:
        write_log(log, 'Couldn\'t remove json dir')
        continue


print()
write_log(log, 'End of programm shutting down machine')
shutdown()
