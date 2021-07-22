from test import main_worker
import argparse
import json
import os
import time

parser = argparse.ArgumentParser(description="STTN")
parser.add_argument("-v", "--video_dir", type=str, required=True)
parser.add_argument("-m", "--mask_dir",   type=str, required=True)
parser.add_argument("-c", "--ckpt",   type=str, required=True)
parser.add_argument("--model",   type=str, default='sttn')
parser.add_argument("--config", type=str, default="configs/davis.json")
args = parser.parse_args()
config = json.load(open(args.config))
print(config)

timings = {}


if __name__ == '__main__':
    for video in sorted(os.listdir(args.video_dir)):
        video_path = args.video_dir + "/" + video
        mask_path = args.mask_dir + "/" + video[:-4]
        start_time = time.time()
        main_worker(video_path, args.ckpt, args.model, mask_path)
        timings[video] = time.time() - start_time
        print("--- %s seconds ---" % (time.time() - start_time))

print(timings)