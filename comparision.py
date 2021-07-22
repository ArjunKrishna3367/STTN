import cv2
from skimage.measure import compare_ssim
from psnr_hvsm import psnr_hvs_hvsm
import numpy as np
from math import sqrt, log10
import sys
import argparse

def PSNR(original, compressed):
    mse = np.mean((original - compressed) ** 2)
    if(mse == 0):  # MSE is zero means no noise is present in the signal .
                  # Therefore PSNR have no importance.
        return 100
    max_pixel = 255.0
    psnr = 20 * log10(max_pixel / sqrt(mse))
    return psnr

def compare(vidPath1, vidPath2, framesPerSec):
    count = 0
    vidcap1 = cv2.VideoCapture(vidPath1)
    vidcap2 = cv2.VideoCapture(vidPath2)
    success1, img1 = vidcap1.read()
    success2, img2 = vidcap2.read()
    success1 = success2 = True
    SSIM_total = 0
    psnr_total = 0
    psnr_total_cv2 = 0
    psnr_hvsm_total = 0

    while success1 and success2:
        image1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        image2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)  # trainImage
        image1 = cv2.resize(image1, image2.shape[::-1])
        score, diff = compare_ssim(image1, image2, full=True, multichannel=False)
        SSIM_total += score
        psnr_total += PSNR(image1, image2)
        psnr_total_cv2 += cv2.PSNR(image1, image2)

        image1 = image1.astype(float) / 255
        image2 = image2.astype(float) / 255
        psnr_hvs, psnr_hvsm = psnr_hvs_hvsm(image1, image2)
        psnr_hvsm_total += psnr_hvsm


        count = count + 1
        vidcap1.set(cv2.CAP_PROP_POS_MSEC, (count * (1 / framesPerSec) * 1000))  # added this line
        success1, img1 = vidcap1.read()
        vidcap2.set(cv2.CAP_PROP_POS_MSEC, (1 / framesPerSec))  # added this line
        success2, img2 = vidcap2.read()

    print("Average SSIM: {}".format(SSIM_total / count))
    # print("Average PSNR: {}".format(psnr_total / count))
    print("Average PSNR (OpenCV): {}".format(psnr_total_cv2 / count))
    print("Average PSNR_HVS_M: {}".format(psnr_hvsm_total / count))


def extractImages(pathIn, pathOut):
    count = 0
    vidcap = cv2.VideoCapture(pathIn)
    success,image = vidcap.read()
    print(success)
    success = True
    while success:
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

