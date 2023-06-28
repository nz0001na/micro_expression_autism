import os
from PIL import Image


# crop input into K pieces
def crop(path, input, height, width):
    im = Image.open(input)
    imgwidth, imgheight = im.size
    k = 0
    for i in range(0, imgheight, height):
        for j in range(0, imgwidth, width):
            box = (j, i, j+width, i+height)
            a = im.crop(box)
            a.save(os.path.join(path, str(k) + '.jpg'))
            k += 1


ro = '7_cleaned_spotted_apex/'
src_path = ro + '1_frames_apex/'
img_size = 224
patch_size = 8

catg_list = os.listdir(src_path)
for catg in catg_list:
    id_list = os.listdir(src_path + catg)
    for ids in id_list:
        sce_list = os.listdir(src_path + catg + '/' + ids)
        for sce in sce_list:
            print(catg + '/' + ids + '/' + sce)
            frm_list = os.listdir(src_path + catg + '/' + ids + '/' + sce)
            for frm in frm_list:
                img_list = os.listdir(src_path + catg + '/' + ids + '/' + sce + '/' + frm)
                for img in img_list:
                    name = img.split('.')[0]
                    dst_path = src_path + catg + '/' + ids + '/' + sce + '/' + frm + '/'
                    dst_fold = dst_path + name
                    if not os.path.exists(dst_fold):
                        os.makedirs(dst_fold)

                    input = src_path + catg + '/' + ids + '/' + sce + '/' + frm + '/' + img
                    crop(dst_fold, input, patch_size, patch_size)
                    print('d')

