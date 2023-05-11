'''
    This code is to detect landmarks of face images
    Envs: dlib_detect
'''

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



predictor_file = 'shape_predictor_68_face_landmarks.dat'
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_file)


ro = '/home/na/3_ASD_micro_expression/2_data_ADOS/'
src_path = ro + '5_cleaned_spotted/1_frames/'
dst_path = ro + '6_cleaned_spotted_landmarks/p_68/'

categ_list = os.listdir(src_path)
for catg in categ_list:
    ids = os.listdir(src_path + catg)
    for id in ids:
        sce_ids = os.listdir(src_path + catg + '/' + id)
        for sce in sce_ids:
            frame_list = os.listdir(src_path + catg + '/' + id + '/' + sce)
            for fra_no in frame_list:
                dst_fold = dst_path + catg + '/' + id + '/' + sce + '/' + fra_no + '/'
                if os.path.exists(dst_fold) is False:
                    os.makedirs(dst_fold)

                img_list = os.listdir(src_path + catg + '/' + id + '/' + sce + '/' + fra_no + '/')
                for img in img_list:
                    print(catg + '/' + id + '/' + sce + '/' + fra_no + '/' + img)
                    img_file = src_path + catg + '/' + id + '/' + sce + '/' + fra_no + '/' + img

                    image = cv2.imread(img_file)
                    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    rects = detector(gray, 1)

                    # may multiple faces in an image
                    if len(rects) < 1:
                        continue

                    landmarks = []
                    landmarks.append(['x', 'y'])
                    shape = predictor(gray, rects[0])
                    shape = shape_to_np(shape)

                    for (x, y) in shape:
                        landmarks.append([str(x), str(y)])
                        cv2.circle(image, (x, y), 1, (0, 0, 255), -1)

                    with open(dst_fold + img.split('.')[0] + '.csv', 'w', newline='') as f:
                        ft = csv.writer(f)
                        ft.writerows(landmarks)

                    cv2.imwrite(dst_fold + img, image)
