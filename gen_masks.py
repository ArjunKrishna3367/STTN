from core.utils import ZipReader, create_random_shape_with_random_motion
import argparse
import random
import cv2
from PIL import Image, ImageOps
import numpy as np
import os
from os import mkdir, path, getcwd

# def get_subdirectory(sd):
#     dir = path.join(getcwd(), f'datasets/testing_masks/{video_name}/')
#     if not path.isdir(dir):
#         mkdir(dir)
#     return dir

def generate_mask(video_name, w, h, dataset):
    all_frames = [f"{str(i).zfill(6)}.jpg" for i in range(1, 100)]

    all_masks = create_random_shape_with_random_motion(len(all_frames), imageHeight=h, imageWidth=w)
    # ref_index = get_ref_index(len(all_frames), sample_length)

    frames = []
    masks = []
    for idx in range(1, 100):
        try:
            img = ZipReader.imread('{}/{}/JPEGImages/{}.zip'.format(
                'datasets', dataset, video_name), all_frames[idx]).convert('RGB')

            img = img.resize((w, h))
            frames.append(img)
            masks.append(all_masks[idx])
        except:
            break

    # fourcc = cv2.VideoWriter_fourcc(*'MP4')
    video = cv2.VideoWriter("datasets/testing/" + video_name + ".avi", 0, 24, (w, h))
    dir = path.join(getcwd(), f'datasets/testing_masks/{video_name}/')
    print(dir)
    if not path.isdir(dir):
        mkdir(dir)

    black = Image.new('RGB', (w, h))
    for i in range(1, 100):
        try:
            mask = masks[i]
            mask.save("datasets/testing_masks/" + video_name + "/" + f"{str(i).zfill(5)}.jpg")
            masked_img = Image.composite(frames[i], black, ImageOps.invert(mask))
            # masked.save("datasets/testing/" + f"{str(i).zfill(5)}.jpg")
            opencv_masked = cv2.cvtColor(np.array(masked_img), cv2.COLOR_RGB2BGR)
            video.write(opencv_masked)
        except:
            break

    video.release()



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
    a.add_argument("--name", help="path to images")
    a.add_argument("--width", help="path to images", type=int)
    a.add_argument("--height", help="path to images", type=int)
    a.add_argument("--dataset", help="path to images")
    args = a.parse_args()

    directory = "datasets/wildlife_360/JPEGImages/"
    for zipped in os.listdir(directory):
        filename = zipped[:-4]
        generate_mask(filename, args.width, args.height, args.dataset)

