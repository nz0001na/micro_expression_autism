"""
    This program extract frames from videos
"""

import cv2
import os
import shutil
import csv

ro = '/home/na/ASD_micro_expression/'
src_path = ro + '2_partition_videos/'
dst_path = ro + '3_frames_raw/'

frame_number = []
subjects = os.listdir(src_path)
for sub in subjects:
    videolist = os.listdir(src_path + sub + '/')
    for videoname in videolist:
        print(sub + '/' + videoname)

        # create dst folder
        frame_dst = dst_path + sub + '/' + videoname.split('.')[0] + '/'
        if(os.path.exists(frame_dst) is False):
            os.makedirs(frame_dst)

        videoCapture = cv2.VideoCapture(src_path + sub + '/' + videoname)
        if (videoCapture.isOpened()):
            print(' Open the video: ' + videoname)
        else:
            print ('Fail to open ' + videoname)

        # fps = videoCapture.get(cv2.CAP_PROP_FPS)

        success, image = videoCapture.read()
        num = 1
        while(success):
            number = "{:06d}".format(num)
            cv2.imwrite(frame_dst + '/frame_' + str(number) + '.jpg', image)
            num = num + 1
            success, image = videoCapture.read()
        frame_number.append([sub, videoname, str(num)])

        videoCapture.release()

with open('frame_count.csv', 'wb') as f:
    ft = csv.writer(f)
    ft.writerows(frame_number)

print('done')
