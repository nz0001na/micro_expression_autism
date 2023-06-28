'''
    This code is to choose the onset and apex frames from ADOS data,
    and make blockwise swapping to generate the swapped image for final feature extraction.
'''
import os
import random
from PIL import Image
import shutil
import math

img_size = 224
patch_size = 8
np = 28

def merge(src_fold):
    # create an empty white picture
    new_im = Image.new('RGB', (img_size, img_size), (250, 250, 250))

    img_list = os.listdir(src_fold + 'swap_70/')
    sorted(img_list)
    for img in img_list:
        im = Image.open(src_fold + 'swap_70/' + img)
        index = int(img.split('.')[0])
        row = int(math.floor(index / 28))
        col = int(index % 28)
        x = row * patch_size
        y = col * patch_size
        new_im.paste(im, (y,x))

    new_im.save(src_fold + 'swap_70.jpg')
    # new_im.show()




ro = '2_data_ADOS/7_cleaned_spotted_apex/'
src_path = ro + '1_frames_apex/'

catg_list = os.listdir(src_path)
for catg in catg_list:
    id_list = os.listdir(src_path + catg)
    for ids in id_list:
        sce_list = os.listdir(src_path + catg + '/' + ids)
        for sce in sce_list:
            print(catg + '/' + ids + '/' + sce)
            frm_list = os.listdir(src_path + catg + '/' + ids + '/' + sce)
            for frm in frm_list:
                src_fold = src_path + catg + '/' + ids + '/' + sce + '/' + frm + '/'
                onset_list = os.listdir(src_fold + 'onset')
                apex_list = os.listdir(src_fold + 'apex')

                dst_fold = src_fold + 'swap_70/'
                if not os.path.exists(dst_fold):
                    os.makedirs(dst_fold)

                count = len(onset_list)
                num_list = list(range(0, count))
                random.shuffle(num_list)

                # swapping ratio (default: 0.5)
                # swapping ratio (0.3, 0.7)
                flag = int(count*0.7)
                for l1 in range(0, flag):
                    shutil.copy(src_fold + 'onset/' + str(num_list[l1]) + '.jpg', dst_fold + str(num_list[l1]) + '.jpg')
                for l1 in range(flag, count):
                    shutil.copy(src_fold + 'apex/' + str(num_list[l1]) + '.jpg', dst_fold + str(num_list[l1]) + '.jpg')

                merge(src_fold)


