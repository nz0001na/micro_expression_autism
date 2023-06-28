'''
    10-fold cross-validation
'''
import os
import scipy.io as sio
from sklearn.svm import SVC
import numpy as np
from sklearn.metrics import f1_score
import random

# 9_cleaned_spotted_mbert_feature_onsetapex
ro = '2_data_ADOS/'
split_path = ro + '10_evaluation/split/folds_2/'
fea_path = ro + '9_cleaned_spotted_feature/9_cleaned_spotted_mbert_feature_swap_50/'
dst_path = ro + '10_evaluation/result_folds_2_shuffle/merge_50/'

sce_list = ['5', '6', '7', '11', '12', '13', '14']
print('******** Merge 30:   *******************')

for sce in sce_list:
    sce_flag = '_' + sce
    dst_fold = dst_path + sce + '/'
    if not os.path.exists(dst_fold):
        os.makedirs(dst_fold)

    print('******** Scene:  ' + sce + '  *******************')

    for i in range(10):
        test_fold = str(i+1)
        print('@@@@@@@@@@ -- Test for fold ' + test_fold + '  @@@@@@@@@@ ')
        train_feature = []
        train_label = []
        test_feature = []
        test_label = []
        test_path = []

        #  read test feature
        f = open(split_path + test_fold + '.txt', 'r')
        test_list = f.readlines()
        for test_id in test_list:
            path = test_id.split('\n')[0].split(' ')[0]
            catg = path.split('/')[0]
            id = path.split('/')[1]
            label = test_id.split('\n')[0].split(' ')[1]
            if not os.path.exists(fea_path + path + '/' + id + sce_flag + '/'):
                continue
            fea_fold = fea_path + path + '/' + id + sce_flag + '/'
            fea_list = os.listdir(fea_fold)
            for fea_file in fea_list:
                data = sio.loadmat(fea_fold + fea_file)
                feature = data['feature'].flatten()
                test_feature.append(feature)
                test_label.append(label)
                test_path.append(path + '/' + id + sce_flag + '/' + fea_file)
        f.close()

        # read train feature
        for j in range(10):
            if j == i: continue
            # print('      ##### -- Train fold ' + str(j+1) + ' #### ')
            ft = open(split_path + str(j+1) + '.txt', 'r')

            train_list = ft.readlines()
            for train_id in train_list:
                path2 = train_id.split('\n')[0].split(' ')[0]
                catg2 = path2.split('/')[0]
                id2 = path2.split('/')[1]
                label2 = train_id.split('\n')[0].split(' ')[1]
                if not os.path.exists(fea_path + path2 + '/' + id2 + sce_flag + '/'):
                    continue
                fea_fold2 = fea_path + path2 + '/' + id2 + sce_flag + '/'
                fea_list2 = os.listdir(fea_fold2)
                for fea_file2 in fea_list2:
                    data2 = sio.loadmat(fea_fold2 + fea_file2)
                    feature2 = data2['feature'].flatten()
                    train_feature.append(feature2)
                    train_label.append(label2)
            ft.close()

        tup1 = np.shape(train_feature)
        tup2 = np.shape(train_label)
        tup3 = np.shape(test_feature)
        tup4 = np.shape(test_label)
        print(tup1)
        # print(tup2)
        print(tup3)
        # print(tup4)

        random.shuffle(test_label)

        # train model
        # print('  @@@@@@ begin training: fold ' + test_fold + '  @@@@ ')
        clf = SVC(kernel='linear', probability=False)
        clf.fit(train_feature, train_label)
        accuracy = clf.score(test_feature, test_label)
        print('Accuracy: {}'.format(accuracy))

        pre_label = clf.predict(test_feature)
        dic = {}
        dic['path'] = test_path
        dic['test_label'] = test_label
        dic['pred_label'] = pre_label
        sio.savemat(dst_fold + test_fold + '.mat', dic)
        print('d')