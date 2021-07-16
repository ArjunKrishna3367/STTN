from core.utils import ZipReader, create_random_shape_with_random_motion
import argparse
import random

def generate_mask(vidpath, video_name, w, h, sample_length):
    all_frames = [f"{str(i).zfill(5)}.jpg" for i in range(video_dict[video_name])]
    all_masks = create_random_shape_with_random_motion(len(all_frames), imageHeight=h, imageWidth=w)


def get_ref_index(length, sample_length):
    if random.uniform(0, 1) > 0.5:
        ref_index = random.sample(range(length), sample_length)
        ref_index.sort()
    else:
        pivot = random.randint(0, length-sample_length)
        ref_index = [pivot+i for i in range(sample_length)]
    return ref_index


if __name__=="__main__":
    a = argparse.ArgumentParser()
    a.add_argument("--path1", help="path to video")
    a.add_argument("--fps", help="path to images", type=int, default=1)
    args = a.parse_args()
    print(args)
    compare(args.path1, args.path2, args.fps)