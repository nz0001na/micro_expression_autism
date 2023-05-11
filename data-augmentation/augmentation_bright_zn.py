'''
this code is to augment face images by:
1. chaning brightness


'''
import imageio
import imgaug as ia
import imgaug.augmenters as iaa
# import numpy as np
# import pandas as pd
# from PIL import Image
# from skimage import data, img_as_float
# from skimage import exposure
import os
# import cv2


ro = 'data_ADOS/7_cleaned_spotted_apex/'
src_path = ro + '4_Not-ASD/'
dst_path = ro + '4_Not-ASD_bright/'

id_list = os.listdir(src_path)
for ids in id_list:
    sce_list = os.listdir(src_path + ids)
    for sce in sce_list:
        print(ids + '/' + sce)
        frm_list = os.listdir(src_path + ids + '/' + sce)
        for frm in frm_list:
            dst_fold = dst_path + ids + '/' + sce + '/' + frm + '/'
            if not os.path.exists(dst_fold):
                os.makedirs(dst_fold)

            img_list = os.listdir(src_path + ids + '/' + sce + '/' + frm)
            for img in img_list:
                img_path = src_path + ids + '/' + sce + '/' + frm + '/' + img
                dst_file = dst_fold + img
                if os.path.exists(dst_file) is True:
                    continue

                image = imageio.imread(img_path)
                # (2) Changing the brightness of the image: GammaContrast
                # Values in the range gamma = (0.5, 2.0) seem to be sensible
                contrast = iaa.GammaContrast(gamma=1.5)
                contrast_image = contrast.augment_image(image)
                imageio.imwrite(dst_file, contrast_image)

