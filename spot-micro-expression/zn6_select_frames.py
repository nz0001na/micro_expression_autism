'''
  Step 6:
  select micro-expression frames from the whole frames of the video
'''

import os
import shutil

ro = '/home/na/3_ASD_micro_expression/'
src_path = ro + '2_cropped/'
dst_path = ro + '4_results/K_17/5_crop_final_apex/'

names = ['EK_190514_Female', 'RH2_181129_Male']
sces = ['_5', '_6', '_7', '_11', '_12', '_13', '_14']


name = names[1]
sub_name = name + sces[6]
print(name + ':' + sub_name)

frame_list = [
[596, 613, 630, 0, 0, 0], [621, 638, 655, 0, 0, 0], [805, 822, 839, 0, 0, 0], [878, 895, 912, 0, 0, 0], [895, 912, 929, 0, 0, 0], [1072, 1089, 1106, 0, 0, 0], [1332, 1349, 1366, 0, 0, 0], [1385, 1402, 1419, 0, 0, 0], [1434, 1451, 1468, 0, 0, 0], [1649, 1666, 1683, 0, 0, 0], [1789, 1806, 1823, 0, 0, 0], [1952, 1969, 1986, 0, 0, 0]


]

src_fold = src_path + name + '/' + sub_name + '/'
dst_fold = dst_path + name + '/' + sub_name + '/'
if os.path.exists(dst_fold) is False:
    os.makedirs(dst_fold)

frames = os.listdir(src_fold)
for listi in range(len(frame_list)):
    item = frame_list[listi]
    sub_fold = 'frames_' + str(listi+1)
    print('  ****   ' + sub_fold)
    dst_subfold = dst_fold + sub_fold + '/'
    if os.path.exists(dst_subfold) is False:
        os.makedirs(dst_subfold)

    start = item[0]*2+1
    end = item[2]*2+1
    for img in range(start, end, 2):
        # img = im*2+1
        img_name = 'frame_' + format(img, '06d') + '.jpg'
        # print(img_name)
        # if img_name in frames:

        src_img = src_fold + img_name
        dst_img = dst_subfold + img_name
        shutil.copy(src_img, dst_img)