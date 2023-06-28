import os
import shutil
import cv2

ro = '7_cleaned_spotted_apex/'
src_path = ro + '1_frames/'
dst_path = ro + '1_frames_apex/'
img_size = 224

catg_list = os.listdir(src_path)
for catg in catg_list:
    id_list = os.listdir(src_path + catg)
    for ids in id_list:
        sce_list = os.listdir(src_path + catg + '/' + ids)
        for sce in sce_list:
            print(catg + '/' + ids + '/' + sce)
            frm_list = os.listdir(src_path + catg + '/' + ids + '/' + sce)
            for frm in frm_list:
                dst_fold = dst_path + catg + '/' + ids + '/' + sce + '/' + frm + '/'
                if not os.path.exists(dst_fold):
                    os.makedirs(dst_fold)
                # if os.path.exists(dst_fold):
                #     continue

                img_list = os.listdir(src_path + catg + '/' + ids + '/' + sce + '/' + frm)
                img_list = sorted(img_list)
                img_path = src_path + catg + '/' + ids + '/' + sce + '/' + frm + '/'

                image_onset = cv2.imread(img_path + img_list[0])
                image_onset = cv2.resize(image_onset, (img_size, img_size))
                cv2.imwrite(dst_fold + 'onset.jpg', image_onset)

                image_apex = cv2.imread(img_path + img_list[17])
                image_apex = cv2.resize(image_apex, (img_size, img_size))
                cv2.imwrite(dst_fold + 'apex.jpg', image_apex)
