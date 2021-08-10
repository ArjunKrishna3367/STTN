from core.utils import ZipReader, create_random_shape_with_random_motion
import argparse
import random
import cv2
from PIL import Image, ImageOps, ImageDraw
import numpy as np
import os
from os import mkdir, path, getcwd
import mask_generators

# def get_subdirectory(sd):
#     dir = path.join(getcwd(), f'datasets/testing_masks/{video_name}/')
#     if not path.isdir(dir):
#         mkdir(dir)
#     return dir

def orig_masks(video_name, w, h, dataset):
    masks = create_random_shape_with_random_motion(100, imageHeight=h, imageWidth=w)
    for i in range(len(masks)):
        masks[i] = ImageOps.invert(masks[i])
    apply_mask(video_name, w, h, dataset, masks, "random")

def stroke_masks(video_name, w, h, dataset):
    masks = mask_generators.get_video_masks_by_moving_random_stroke(video_len=100, imageWidth=w, imageHeight=h, brushWidthBound=(40, 50), nStroke=10)
    apply_mask(video_name, w, h, dataset, masks, "stroke")

def bounding_box_masks(video_name, w, h, dataset):
    sizeX = random.randrange(4, 6)/10
    sizeY = random.randrange(4, 6)/10
    startCoords = (random.randrange(0, w) / 2, random.randrange(0, h)/2)
    endCoords = startCoords[0] + sizeX * w, startCoords[1] + sizeY * h
    mask = Image.new("L", (w, h), 255)
    draw = ImageDraw.Draw(mask)
    draw.rectangle((startCoords, endCoords), fill=0)
    masks = [mask] * 100
    apply_mask(video_name, w, h, dataset, masks, "box")

def apply_mask(video_name, w, h, dataset, masks, maskType):
    all_frames = [f"{str(i).zfill(6)}.jpg" for i in range(1, 100)]
    frames = []
    for idx in range(1, 100):
        try:
            img = ZipReader.imread('{}/{}/JPEGImages/{}.zip'.format(
                'datasets', dataset, video_name), all_frames[idx]).convert('RGB')

            img = img.resize((w, h))
            frames.append(img)
        except:
            break

    video = cv2.VideoWriter("examples/testing/" + video_name + "_" + maskType + ".avi", 0, 24, (w, h))
    dir = path.join(getcwd(), f'examples/testing_masks/{video_name}/')
    if not path.isdir(dir):
        mkdir(dir)

    black = Image.new('RGB', (w, h))

    for i in range(1, 100):
        try:
            mask = masks[i].convert('L')
            mask.save("examples/testing_masks/" + video_name + "/" + f"{str(i).zfill(5)}.jpg")
            masked_img = Image.composite(frames[i], black, mask)
            # masked.save("datasets/testing/" + f"{str(i).zfill(5)}.jpg")
            opencv_masked = cv2.cvtColor(np.array(masked_img), cv2.COLOR_RGB2BGR)
            video.write(opencv_masked)
        except:
            print("fail")
            break

    video.release()



if __name__=="__main__":
    a = argparse.ArgumentParser()
    a.add_argument("--width", help="path to images", type=int)
    a.add_argument("--height", help="path to images", type=int)
    a.add_argument("--dataset", help="path to images")
    args = a.parse_args()

    directory = "datasets/wildlife_360/JPEGImages/"
    for zipped in os.listdir(directory):
        filename = zipped[:-4]
        orig_masks(filename, args.width, args.height, args.dataset)
        # stroke_masks(filename, args.width, args.height, args.dataset)
        # bounding_box_masks(filename, args.width, args.height, args.dataset)
        print(filename, "saved")

    # get_random_walk_mask(args.width, args.height, 1)

