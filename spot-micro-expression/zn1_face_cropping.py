'''
 Step 1:
 This code is to crop face area using the bounding box of the 1st frame of each video
'''

import os
import dlib
import cv2

detector = dlib.get_frontal_face_detector()


def rect_to_bb(rect):
    x = rect.left()
    y = rect.top()
    w = rect.right() - x
    h = rect.bottom() - y
    return (x, y, w, h)

def rect_to_bb2(rect):
    left = rect.left()
    top = rect.top()
    right = rect.right()
    bottom = rect.bottom()
    return (left, top, right, bottom)


def cropping(src_path, dst_path, left, top, right, bottom):
    img_list = os.listdir(src_path)
    for img in img_list:
        if os.path.exists(dst_path + img): continue
        num = int(img.split('.')[0].split('_')[1])
        if num % 2 == 0: continue

        image = cv2.imread(src_path + img)
        face = image[top:bottom, left:right]  # Crop the face region
        face = cv2.resize(face, (128, 128))  # Resize to 128x128
        cv2.imwrite(dst_path + img, face)


if __name__ == '__main__':
    ro = '/home/na/3_ASD_micro_expression/2_data_ADOS/1_TN/'
    names = ['MP_190509_Female']
    sces = [5, 6, 7, 11, 12, 13, 14]

    sub_name = names[0]
    for sce in sces:
        print(names[0] + ':' + str(sce))
        fold_name = sub_name + '_' + str(sce)
        src_path = ro + '4_raw/'+sub_name+'/' + fold_name + '/'
        dst_path = ro + '4_cropped/'+sub_name+'/' + fold_name + '/'
        if os.path.exists(dst_path) is False:
            os.makedirs(dst_path)

        left = 165
        top = 75
        right = 425
        bottom = 335
        cropping(src_path, dst_path, left, top, right, bottom)
    print('done')