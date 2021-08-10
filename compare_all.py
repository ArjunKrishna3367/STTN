from comparision import compare
import argparse
import json
import os
import time
import csv

parser = argparse.ArgumentParser(description="STTN")
parser.add_argument("-o", "--orig_video_dir", type=str, required=True)
parser.add_argument("-n", "--new_video_dir",   type=str, required=True)
parser.add_argument("--model_name", type=str)
args = parser.parse_args()


scores = {}
if __name__ == '__main__':
    for video in sorted(os.listdir(args.orig_video_dir)):
        orig_video_path = args.orig_video_dir + "/" + video
        new_video_path = "{}/{}_result_{}.mp4".format(args.new_video_dir, video[:-4], args.model_name)
        try:
            scores[video] = compare(orig_video_path, new_video_path, 24)
        except:
            print("failed")

print(scores)

keys = sorted(scores.keys())
with open('scores_' + args.model_name + ".csv", "w") as file:
        writer = csv.writer(file, delimiter = "\t")
        writer.writerow(keys)
        writer.writerows(zip(*[scores[key] for key in keys]))