'''
 Step 4:
 calculate pseudo-label of data
'''


import numpy as np
import scipy.io as sio
import cv2
import os


def load_images(src_path):
    final_images = []
    images = []
    imgs = os.listdir(src_path)
    imgs.sort()
    for img in imgs:
        # print('    ' + img)
        image = cv2.imread(src_path + img, 0)
        images.append(image)

    final_images.append(np.array(images))
    return final_images

# Step 5: pseudo-label
def pseudo_labeling(final_images, final_samples, k):
    pseudo_y = []
    video_count = 0

    samples_arr = []
    video = []
    if (len(video) == 0):
        # Last k frames are ignored
        pseudo_y.append([0 for i in range(len(final_images[video_count]) - k)])
    else:
        pseudo_y_each = [0] * (len(final_images[video_count]) - k)
        for ME in video:
            samples_arr.append(np.arange(ME[0] + 1, ME[1] + 1))
        for ground_truth_arr in samples_arr:
            for index in range(len(pseudo_y_each)):
                pseudo_arr = np.arange(index, index + k)
                # Equivalent to if IoU>0 then y=1, else y=0
                if (pseudo_y_each[index] < len(np.intersect1d(pseudo_arr, ground_truth_arr)) / len(
                        np.union1d(pseudo_arr, ground_truth_arr))):
                    pseudo_y_each[index] = 1
        pseudo_y.append(pseudo_y_each)
    video_count += 1

    # Integrate all videos into one dataset
    pseudo_y = [y for x in pseudo_y for y in x]
    print('Total frames:', len(pseudo_y))
    return pseudo_y


if __name__ == '__main__':
    k = 17  # CASME_sq:17,  SAMMLV:159

    ro = '/home/na/3_ASD_micro_expression/2_data_ADOS/1_TN/'
    names = ['EK_190514_Female', 'RH2_181129_Male']
    sces = ['_5', '_6', '_7', '_11', '_12', '_13', '_14']

    for name in names:
        for sce in sces:
            print(name + ':' + sce)
            src_path = ro + '4_cropped/'+name+'/'+name+sce+'/'
            dst_path = ro + '3_OF_feature/K_17/'+name+'/'+name+sce+'/'
            if os.path.exists(dst_path) is False:
                os.makedirs(dst_path)
        
            final_images = load_images(src_path)
            final_samples = ['onset', 'offset'] #???
        
            pseudo_y = pseudo_labeling(final_images, final_samples, k)
        
            data = {}
            data['label'] = pseudo_y
            sio.savemat(dst_path + name+sce+'_y.mat', data)
            print('d')
