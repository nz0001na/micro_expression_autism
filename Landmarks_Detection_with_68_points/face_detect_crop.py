#/*
#  This code is for facial bbox detection
# */

import numpy as np
import argparse
import cv2
import dlib
import imutils
import os
import csv

def rect_to_bb(rect):
    x = rect.left()
    y = rect.top()
    w = rect.right() - x
    h = rect.bottom() - y
    return (x, y, w, h)


def shape_to_np(shape, dtype="int"):
    coords = np.zeros((68, 2), dtype=dtype)

    for i in range(68):
        coords[i] = (shape.part(i).x, shape.part(i).y)
    return coords



ro = '/home/na/ASD_micro_expression/'
src_path = ro + '3_frames_raw/'
dst_path = ro + '9_cleaned_spotted_crop_face/'

if os.path.exists(dst_path) is False: os.makedirs(dst_path)

predictor_file = 'shape_predictor_68_face_landmarks.dat'
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_file)


levels = os.listdir(src_path)
for level in levels:
    ids = os.listdir(src_path + level)
    for id in ids:
        # print(level + '/' + id)
        secs = os.listdir(src_path + level + '/' + id)
        for sec in secs:
            frams = os.listdir(src_path + level + '/' + id + '/' + sec)
            for frm in frams:
                dst_fold = dst_path + level + '/' + id + '/' + sec + '/' + frm + '/'
                if os.path.exists(dst_fold) is False:
                    os.makedirs(dst_fold)

                img_list = os.listdir(src_path + level + '/' + id + '/' + sec + '/' + frm)
                for img in img_list:
                    if os.path.exists(dst_fold + img) is True: continue
                    if os.path.exists(dst_fold + img) is False:
                        print(level + '/' + id + '/' + sec + '/' + frm + '/' + img)
                    img_path = src_path + level + '/' + id + '/' + sec + '/' + frm + '/' + img
                    image = cv2.imread(img_path)
                    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    rects = detector(gray, 1)

                    # may multiple faces in an image
                    if len(rects) < 1:
                        continue
                    rect = rects[0]

                    (x, y, w, h) = rect_to_bb(rect)
                    x1 = x+w
                    y1 = y+h

                    if w != h: h = w
                    size = w
                    crop_img = image[y:y+h, x:x+w]
                    resized = cv2.resize(crop_img, (128, 128), interpolation=cv2.INTER_AREA)
                    cv2.imwrite(dst_fold + img, resized)


