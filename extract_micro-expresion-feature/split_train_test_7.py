'''
    10-fold cross-validation for binary classification
    0: ASD
    1: NT
'''

import os
import random


ro = '2_data_ADOS/'
src_path = ro + '9_cleaned_spotted_mbert_feature/'
dst_path = ro + '10_evaluation/split/'
if not os.path.exists(dst_path):
    os.makedirs(dst_path)

asd_list = ['1_Autism', '2_Autism-Spectrum', '3_Non-Spectrum']
nt_list = ['4_Not-ASD', '4_Not-ASD_bright', '4_Not-ASD_flip', '4_Not-ASD_hiseql']

f = open('asd_list.txt', 'w')
f2 = open('nt_list.txt', 'w')
f3 = open('fold.txt', 'w')

def split_10fold(src_path):
    asd_id_list = []
    for asd in asd_list:
        id_list = os.listdir(src_path + asd)
        for id in id_list:
            f.write(asd + '/' + id + ' 0\n')
            asd_id_list.append(asd + '/' + id + ' 0\n')

    nt_id_list = []
    for nt in nt_list:
        id_list = os.listdir(src_path + nt)
        for id in id_list:
            f2.write(nt + '/' + id + ' 1\n')
            nt_id_list.append(nt + '/' + id + ' 1\n')

    random.shuffle(nt_id_list)
    random.shuffle(asd_id_list)
    f3.writelines(asd_id_list)
    f3.writelines(nt_id_list)


split_10fold(src_path)
f.close()
f2.close()
f3.close()
print('d')