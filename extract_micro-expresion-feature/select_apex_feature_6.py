'''
choose feature file of apex and onset for each segment
'''

import os
import shutil

ro = '2_data_ADOS/'
src_path = ro + '9_cleaned_spotted_mbert_feature/'
dst_path = ro + '9_cleaned_spotted_mbert_feature_onsetapex/'


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
                if os.path.exists(dst_fold):
                    continue
                if not os.path.exists(dst_fold):
                    os.makedirs(dst_fold)

                src_fold = src_path + catg + '/' + ids + '/' + sce + '/' + frm + '/'
                img_list = os.listdir(src_fold)
                sorted(img_list)
                shutil.copy(src_fold + img_list[0], dst_fold + 'onset.mat')
                shutil.copy(src_fold + img_list[17], dst_fold + 'apex.mat')

