import cv2
from skimage.measure import compare_ssim

import sys
import argparse

def compare(vidPath1, vidPath2, framesPerSec):
    count = 0
    vidcap1 = cv2.VideoCapture(vidPath1)
    vidcap2 = cv2.VideoCapture(vidPath2)
    success1, img1 = vidcap1.read()
    success2, img2 = vidcap2.read()
    success1 = success2 = True

    while success1 and success2:
        print('Read a new frame: ', success1, success2)
        image1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        image2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)  # trainImage
        score, diff = compare_ssim(image1, image2, full=True, multichannel=False)
        print("SSIM: {}".format(score))
        count = count + 1
        vidcap1.set(cv2.CAP_PROP_POS_MSEC, (count * (1 / framesPerSec) * 1000))  # added this line
        success1, img1 = vidcap1.read()
        vidcap2.set(cv2.CAP_PROP_POS_MSEC, (1 / framesPerSec))  # added this line
        success2, img2 = vidcap2.read()


def extractImages(pathIn, pathOut):
    count = 0
    vidcap = cv2.VideoCapture(pathIn)
    success,image = vidcap.read()
    print(success)
    success = True
    while success:
        print ('Read a new frame: ', success)
        cv2.imwrite( pathOut + "\\frame%d.jpg" % count, image)     # save frame as JPEG file
        count = count + 1
        vidcap.set(cv2.CAP_PROP_POS_MSEC, (count * 1000))  # added this line
        success, image = vidcap.read()

if __name__=="__main__":
    a = argparse.ArgumentParser()
    a.add_argument("--path1", help="path to video")
    a.add_argument("--path2", help="path to images")
    a.add_argument("--fps", help="path to images", type=int, default=1)
    args = a.parse_args()
    print(args)
    compare(args.path1, args.path2, args.fps)
    # extractImages(args.path1, "/")

