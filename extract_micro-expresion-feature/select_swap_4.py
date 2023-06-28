'''
Select swaped frames
'''

import os
import shutil

ro = '2_data_ADOS/7_cleaned_spotted_apex/'
src_path = ro + '1_frames_apex/'
dst_path = ro + '1_frames_swap_70/'

catg_list = os.listdir(src_path)
for catg in catg_list:
    id_list = os.listdir(src_path + catg)
    for ids in id_list:
        sce_list = os.listdir(src_path + catg + '/' + ids)
        for sce in sce_list:
            print(catg + '/' + ids + '/' + sce)

            dst_fold = dst_path + catg + '/' + ids + '/' + sce + '/'
            if not os.path.exists(dst_fold):
                os.makedirs(dst_fold)

            frm_list = os.listdir(src_path + catg + '/' + ids + '/' + sce)
            for frm in frm_list:
                src_fold = src_path + catg + '/' + ids + '/' + sce + '/' + frm + '/'
                src_img = src_fold + 'swap_70.jpg'
                shutil.copy(src_img, dst_fold + frm + '_swap_70.jpg')

