import os
import shutil
import glob
import natsort
import pickle
import dlib
import numpy as np
import cv2

# Step 1:  detect and crop frames
def crop_images(dataset_name):
    face_detector = dlib.get_frontal_face_detector()
    if dataset_name == 'CASME_sq':
        sub_list = os.listdir(dataset_name + '/rawpic/')
        for subjectName in sub_list:
            dataset_rawpic = dataset_name + '/rawpic/' + subjectName + '/'
            dir_crop_sub = dataset_name + '/rawpic_crop/' + subjectName + '/'

            # Create new directory for each video
            vid_list = os.listdir(dataset_name + '/rawpic/' + subjectName + '/')
            for vid in vid_list:
                dir_crop_sub_vid = dir_crop_sub + vid + '/' # Get dir of video
                if os.path.exists(dir_crop_sub_vid) is False:
                    os.makedirs(dir_crop_sub_vid)

                # Use first frame as reference frame
                first_img = dataset_name + '/rawpic/' + subjectName + '/' + vid + '/img001.jpg'
                image1 = cv2.imread(first_img)
                # Run the HOG face detector on the image data
                detected_face1 = face_detector(image1, 1)
                # print(detected_face1)
                for face in detected_face1:
                    face_top = face.top()
                    face_bottom = face.bottom()
                    face_left = face.left()
                    face_right = face.right()

                img_list = os.listdir(dataset_name + '/rawpic/' + subjectName + '/' + vid)
                for img in img_list:
                    if os.path.exists(dir_crop_sub_vid + img): continue
                    if img != 'img001.jpg': continue
                    if img[-3:] != 'jpg': continue
                    # count = img[3:-4]
                    # # Load the image
                    image = cv2.imread(dataset_rawpic + vid + '/' + img)
                    face = image[face_top:face_bottom, face_left:face_right]  # Crop the face region
                    print(subjectName + ':' + vid +':'+img)
                    face = cv2.resize(face, (128, 128))  # Resize to 128x128
                    cv2.imwrite(dir_crop_sub_vid + img, face)

    elif dataset_name == 'SAMMLV':
        dir_crop = dataset_name + '/SAMM_longvideos_crop/'
        src_path = dataset_name + '/SAMM_longvideos/'
        vid_list = os.listdir(src_path)
        for vid in vid_list:
            if vid == '016_7': continue
            print(vid)
            dir_crop_vid = dir_crop + vid + '/'
            if os.path.exists(dir_crop_vid) is False:
                os.makedirs(dir_crop_vid)

            # Use first frame as reference frame
            first_img = src_path + vid + '/' + vid + '_0001.jpg'
            image1 = cv2.imread(first_img)
            detected_face1 = face_detector(image1, 1)
            # print(detected_face1)
            for face in detected_face1:
                face_top = face.top()
                face_bottom = face.bottom()
                face_left = face.left()
                face_right = face.right()

            img_list = os.listdir(src_path + vid + '/')
            for img in img_list:
                if os.path.exists(dir_crop_vid + img): continue
                if img == vid + '_0001.jpg': continue
                if img[-3:] != 'jpg': continue
                # count = img[3:-4]
                image = cv2.imread(src_path + vid + '/' + img)
                face = image[face_top:face_bottom, face_left:face_right]  # Crop the face region
                print(vid + ':' + img)
                face = cv2.resize(face, (128, 128))  # Resize to 128x128
                cv2.imwrite(dir_crop_vid + img, face)

    
# Step 2: load data
def load_images(dataset_name):
    images = []
    subjects = []
    subjectsVideos = []
    
    if dataset_name == 'CASME_sq':
        dir_subs = os.listdir(dataset_name + "/rawpic_crop")
        dir_subs.sort()
        for dir_sub in dir_subs:
            print(dir_sub)
            subjects.append(dir_sub)
            # subjectsVideos.append([])

            dir_sub_vids = os.listdir(dataset_name + "/rawpic_crop/" + dir_sub)
            dir_sub_vids.sort()
            for dir_sub_vid in dir_sub_vids:
                subjectsVideos.append(dir_sub_vid.split('_')[1][:4])
                image = []
                dst = dataset_name + "/rawpic_crop/" + dir_sub + '/' + dir_sub_vid + '/'
                imgs = os.listdir(dst)
                for img in imgs:
                    image.append(cv2.imread(dst + img, 0))
                images.append(np.array(image))





        # for i, dir_sub in enumerate(natsort.natsorted(glob.glob(dataset_name + "\\rawpic_crop\\*"))):
        #   print('Subject: ' + dir_sub.split('\\')[-1])
        #   subjects.append(dir_sub.split('\\')[-1])
        #   subjectsVideos.append([])
        #   for dir_sub_vid in natsort.natsorted(glob.glob(dir_sub + "\\*")):
        #       # Ex:'CASME_sq/rawpic_aligned/s15/15_0101disgustingteeth' -> '0101'
        #     subjectsVideos[-1].append(dir_sub_vid.split('\\')[-1].split('_')[1][:4])
        #     image = []
        #     for dir_sub_vid_img in natsort.natsorted(glob.glob(dir_sub_vid + "\\img*.jpg")):
        #       image.append(cv2.imread(dir_sub_vid_img, 0))
        #     images.append(np.array(image))
        
    elif dataset_name == 'SAMMLV':
        for i, dir_vid in enumerate(natsort.natsorted(glob.glob(dataset_name + "\\SAMM_longvideos_crop\\*"))):
          print('Subject: ' + dir_vid.split('\\')[-1].split('_')[0])
          subject = dir_vid.split('\\')[-1].split('_')[0]
          subjectVideo = dir_vid.split('\\')[-1]
          if (subject not in subjects): # Only append unique subject name
            subjects.append(subject)
            subjectsVideos.append([])
          subjectsVideos[-1].append(dir_vid.split('\\')[-1])
    
          image = []
          for dir_vid_img in natsort.natsorted(glob.glob(dir_vid + "\\*.jpg")):
            image.append(cv2.imread(dir_vid_img, 0))
          image = np.array(image)
          images.append(image)
    
    return images, subjects, subjectsVideos

#
def save_images_pkl(dataset_name, images, subjectsVideos, subjects):
    pickle.dump(images, open(dataset_name + "_images_crop.pkl", "wb") )
    pickle.dump(subjectsVideos, open(dataset_name + "_subjectsVideos_crop.pkl", "wb") )
    pickle.dump(subjects, open(dataset_name + "_subjects_crop.pkl", "wb") )

def load_images_pkl(dataset_name):
    images = pickle.load( open( dataset_name + "_images_crop.pkl", "rb" ) )
    subjectsVideos = pickle.load( open( dataset_name + "_subjectsVideos_crop.pkl", "rb" ) )
    subjects = pickle.load( open( dataset_name + "_subjects_crop.pkl", "rb" ) )
    return images, subjectsVideos, subjects



