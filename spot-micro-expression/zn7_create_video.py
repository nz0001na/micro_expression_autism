'''
  Step 7:
  use selected frames to create videos
'''


import os
import moviepy.video.io.ImageSequenceClip

ro = '/home/na/3_ASD_micro_expression/'
src_path = ro + '4_results/K_17/5_crop_final_apex/'
dst_path = ro + '4_results/K_17/6_crop_final_apex_video/'
fps = 30

names = ['EK_190514_Female', 'RH2_181129_Male']
sces = ['_5', '_6', '_7', '_11', '_12', '_13', '_14']


for name in names:
    for sce in sces:
        sub_name = name + sce
        print(sub_name)
        dst_fold = dst_path + name + '/' + sub_name + '/'
        if os.path.exists(dst_fold) is False:
            os.makedirs(dst_fold)

        src_fold = src_path + name + '/' + sub_name + '/'
        sub_videos = os.listdir(src_fold)
        for subv in sub_videos:
            print('   :' + subv)
            dst_video = dst_fold + subv + '.mp4'

            imgs = os.listdir(src_fold + subv)
            imgs.sort()
            image_files = [os.path.join(src_fold + subv, img)
                           for img in imgs
                           if img.endswith(".jpg")]
            clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps=fps)
            clip.write_videofile(dst_video)