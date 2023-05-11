'''
This code is to predict ASD videos using pre-trained model for micro-expression spotting

/home/na/3_ASD_micro_expression/1_code/SoftNet-SpotME-main/SAMMLV/SAMM_longvideos/016_7

'''


import sys
import argparse
from load_images import *
from load_label import *
from extraction_preprocess import *
from training import *

## Note that the whole process will take a long time... please be patient
def main(config):
    # Define the dataset and expression to spot
    dataset_name = config.dataset_name
    expression_type = config.expression_type
    train = config.train
    show_plot = config.show_plot
    
    print(' ------ Spotting', dataset_name, expression_type, '-------')

    # print('1. Croping Images --------------')
    # crop_images(dataset_name)

    print("2. Loading Images --------------")
    images, subjects, subjectsVideos = load_images(dataset_name)
    #images = pickle.load( open( dataset_name + "_images_crop.pkl", "rb" ) )

    print('3. Loading Excel ------------------')
    codeFinal = load_excel(dataset_name)
    print('  3.1. Loading Ground Truth From Excel ------')
    final_images, final_videos, final_subjects, final_samples = load_gt(dataset_name, expression_type, images, subjectsVideos, subjects, codeFinal) 
    print('  3.2. Computing k ------')
    k = cal_k(dataset_name, expression_type, final_samples)

    print('4. Feature Extraction & Pre-processing ------------')
    dataset = extract_preprocess(final_images, k)

    print('5. Pseudo-Labeling ------------')
    pseudo_y = pseudo_labeling(final_images, final_samples, k)

    print('6. LOSO: Leave one Subject Out ------------')
    X, y, groupsLabel = loso(dataset, pseudo_y, final_images, final_samples, k)

    print('7. SOFTNet Training ------------')
    TP, FP, FN, metric_fn = training(X, y, groupsLabel, dataset_name, expression_type, final_samples, k, dataset, train, show_plot)

    print('8. SOFTNet Testing ------------')
    final_evaluation(TP, FP, FN, metric_fn)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # input parameters
    # Specify CASME_sq or SAMMLV only
    parser.add_argument('--dataset_name', type=str, default='CASME_sq')
    # Specify micro-expression or macro-expression only
    parser.add_argument('--expression_type', type=str, default='micro-expression')
    # Train or use pre-trained weight for prediction
    parser.add_argument('--train', type=bool, default=False)
    parser.add_argument('--show_plot', type=bool, default=True)
    
    config = parser.parse_args()

    main(config)
