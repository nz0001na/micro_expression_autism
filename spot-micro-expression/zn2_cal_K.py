'''
  Step 2:
  This code is to calculate k value
'''

import numpy as np
import pandas as pd

# Step 3:  3.2. Computing k
def cal_k(samples):
    total_duration = 0
    for sample in samples:
        total_duration += sample[1]-sample[0]
    N = total_duration / len(samples)
    k = int((N+1)/2)
    print('k (Half of average length of expression) =', k)
    return k

if __name__ == '__main__':
    dataset_name = 'SAMMLV'  # CASME_sq   'SAMMLV'

    # SAMM_LV_code_final  casme_sq_code_final
    exl_file = 'labels/SAMM_LV_code_final.xlsx'

    xl = pd.ExcelFile(exl_file)

    # # CASME_sq
    # colsName = ['subject', 'video', 'onset', 'apex', 'offset', 'au', 'emotion', 'type', 'selfReport']
    # codeFinal = xl.parse(xl.sheet_names[0], header=None, names=colsName)  # Get data
    # apexs = codeFinal.apex
    # onsets = codeFinal.onset
    # offsets = codeFinal.offset

    ## SAMMLV
    colsName = ['Subject', 'Filename', 'Inducement Code', 'Onset', 'Apex', 'Offset', 'Duration', 'Type', 'Action Units',
                'Notes']
    codeFinal = xl.parse(xl.sheet_names[0], header=None, names=colsName, skiprows=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    apexs = codeFinal.Apex
    onsets = codeFinal.Onset
    offsets = codeFinal.Offset

    count = len(onsets)
    on_off = []
    for i in range(count):
        onset = onsets[i]
        offset = offsets[i]
        if offset == 0: continue
        on_off.append([int(onset - 1), int(offset - 1)])

    K = cal_k(on_off)
    print(K)