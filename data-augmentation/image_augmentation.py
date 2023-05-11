'''
this code is to augment face images by:
1. flipping
2.

'''
import imageio
import imgaug as ia
import imgaug.augmenters as iaa
import numpy as np
import pandas as pd
from PIL import Image
from skimage import data, img_as_float
from skimage import exposure
import os
import cv2


ro = '/home/na/'
src_path = ro + 'data/'

# dst_path = ro + 'flipping/'
# dst_path = ro + 'brightness15/'
# dst_path = ro + 'brightness5/'
# dst_path = ro + 'brightsigmoid6/'
# dst_path = ro + 'brightlinear4/'
# dst_path = ro + 'resizing/'
# dst_path = ro + 'resizing2/'
# dst_path = ro + 'jpgcompress15/'
dst_path = ro + 'jpgcompress25/'
# dst_path = ro + 'histeql/'

if os.path.exists(dst_path) is False:
    os.makedirs(dst_path)

img_list = os.listdir(src_path)
for i in range(len(img_list)):
    img_name = img_list[i]
    new_name = img_name.split('.')[0] + '_comp3.jpg'

    # image = imageio.imread(src_path + img_name)
    image = Image.open(src_path + img_name)
    # image = cv2.imread(src_path + img_name)
    # ia.imshow(image)

    # # (1) # flipping image horizontally
    # flip_hr = iaa.Fliplr(p=1.0)
    # flip_hr_image = flip_hr.augment_image(image)
    # imageio.imwrite(dst_path + new_name,flip_hr_image)

    # # (2) Changing the brightness of the image: GammaContrast
    # # Values in the range gamma = (0.5, 2.0) seem to be sensible
    # contrast = iaa.GammaContrast(gamma=1.5)
    # contrast_image = contrast.augment_image(image)
    # imageio.imwrite(dst_path + new_name, contrast_image)

    # # (3) Changing the brightness of the image: SigmoidContrast
    # # Values in the range gain = (5, 20) and cutoff = (0.25, 0.75) seem to be sensible.
    # # (10, 0.5) (10, 0.35) (10, 0.65) (15, 0.5) (15, 0.35) (13, 0.5)
    # contrast = iaa.SigmoidContrast(gain=13, cutoff=0.5)
    # contrast_image = contrast.augment_image(image)
    # imageio.imwrite(dst_path + new_name, contrast_image)

    # # (4) Changing the brightness of the image: LinearContrast
    # # alpha=(0.4, 1.6)
    # # (0.6)  (0.8)  (1.0)  (1.2)
    # contrast = iaa.LinearContrast(alpha=1.2)
    # contrast_image = contrast.augment_image(image)
    # imageio.imwrite(dst_path + new_name, contrast_image)

    # # (5) Scaling the image
    # scale_im = iaa.Affine(scale={"x": (1.5, 1.0), "y": (1.5, 1.0)})
    # scale_image = scale_im.augment_image(image)

    # # (6) resize the image: (413, 531) to (480, 500)
    # img = image.resize((470, 531))
    # img.save(dst_path + new_name)

    # (7) JPEG Compression with a high quality factor
    # The more the value of quality variable and lesser the compression
    # image.save(dst_path + new_name, "JPEG", optimize=True, quality=25)

    # # (8) histogram equalization
    # src = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # dst = cv2.equalizeHist(src)
    # cv2.imwrite(dst_path + new_name, dst)


    # ia.imshow(contrast_image)



    print('done')

