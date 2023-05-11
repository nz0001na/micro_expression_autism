'''
  Step 5:
  spotting micro-expression by predicting scores of frames
'''

from training import *
import scipy.io as sio
import csv

def predict_data(model, model_path, X_test, y_test, batch_size):
    model.load_weights(model_path)  # Load Pretrained Weights

    result = model.predict_generator(
        generator(X_test, y_test, batch_size),
        steps=len(X_test) / batch_size,
        verbose=1
    )

    return result


# features : dataset
# subject_count:
# spotting
def spotting(result, subject_count, dataset, k, p, show_plot):
    prev = 0
    preds = []

    score_plot = np.array(
        result[prev:prev + len(dataset)])  # Get related frames to each video
    score_plot_agg = score_plot.copy()

    # Score aggregation
    for x in range(len(score_plot[k:-k])):
        score_plot_agg[x + k] = score_plot[x:x + 2 * k].mean()
    score_plot_agg = score_plot_agg[k:-k]

    # Plot the result to see the peaks
    # Note for some video the ground truth samples is below frame index 0 due to the effect of aggregation, but no impact to the evaluation
    if show_plot:
        plt.figure(figsize=(15, 4))
        plt.plot(score_plot_agg)
        plt.xlabel('Frame')
        plt.ylabel('Score')

    # Moilanen threshold technique
    threshold = score_plot_agg.mean() + p * (max(score_plot_agg) - score_plot_agg.mean())
    print(threshold)
    peaks, _ = find_peaks(score_plot_agg[:, 0], height=threshold[0], distance=k)
    # Occurs when no peak is detected, simply give a value to pass the exception in mean_average_precision
    if len(peaks) == 0:
        preds.append([0, 0, 0, 0, 0, 0])
    for peak in peaks:
        # Extend left and right side of peak by k frames
        preds.append([peak - k, peak, peak + k, 0, 0, 0])
        # preds.append([peak - k, 0, peak + k, 0, 0, 0])
    if show_plot:
        plt.show()
    prev += len(dataset)
    return preds



if __name__ == '__main__':
    # Specify CASME_sq or SAMMLV only
    dataset_name = 'CASME_sq'  # 'SAMMLV'  CASME_sq
    # Specify micro-expression or macro-expression only
    expression_type = 'micro-expression'  # micro-expression   macro-expression
    subject_count = 's14'
    model_path = 'pretrain_weights/' + dataset_name + '/' + expression_type + '/' + str(subject_count) + '.hdf5'

    subject_count = 0
    epochs = 10
    batch_size = 12
    k = 17
    p = 0.55  # From our analysis, 0.55 achieved the highest F1-Score
    show_plot = True
    model = SOFTNet()

    names = ['EK_190514_Female', 'RH2_181129_Male']
    sces = ['_5', '_6', '_7', '_11', '_12', '_13', '_14']


    ro = '/home/na/3_ASD_micro_expression/3_OF_feature/K_17/'
    for name in names:
        for sce in sces:
            sub_name = name + sce
            print(sub_name)
            dst_path = ro + name + '/' + sub_name + '/'
            dst_file = dst_path + sub_name + '_score.csv'

            features_data = sio.loadmat(ro + name + '/'+sub_name+'/'+sub_name+'.mat')
            feature = features_data['fea'][0]
            label_data = sio.loadmat(ro + name + '/'+sub_name+'/'+sub_name+'_y.mat')
            label = label_data['label']

            result = predict_data(model, model_path, feature, label, batch_size)
            with open(dst_file, 'w', newline='') as f:
                ft = csv.writer(f)
                ft.writerows(result)

            preds = spotting(result, subject_count, feature, k, p, show_plot)
            print(preds)

            print('done')



