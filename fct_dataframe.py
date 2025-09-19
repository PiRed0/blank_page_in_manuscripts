def determine_accurency(row, pval_type, threshold, gt_type):
    '''
    pd.Series * str * float * str -> str
    '''
    if row[pval_type] < threshold and row[gt_type] == 'written':
        accurency = 'TP'
    elif row[pval_type] < threshold and row[gt_type] == 'blank':
        accurency = 'FP'
    elif row[pval_type] >= threshold and row[gt_type] == 'written':
        accurency = 'FN'
    else:
        accurency = 'TN'
    return accurency