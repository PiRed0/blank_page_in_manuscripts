import numpy as np
from fct_sampling import list_of_n_randpixels
from fct_gmm import gmm_data_dict, gmm_repartition_function
from fct_h0 import test_dist_means, add_h0_dict



def compute_page_gmm(pm, page, gmm_data, img_array, x, nbr_samples, nbr_pix, nbr_comp, nbr_sigma):
    '''
    str * int * Dict[str, Dict[int, Dict[int, Dict[str, T]]]] * np.2darray * np.1darray * int * int * int * float ->
    Dict[str, Dict[int, Dict[int, Dict[str, T]]]]
    Update the dictionnary gmm_data with nbr_samples GMMs for the page of the manuscript pm
    given img_array, x, nbr_pix, nbr_comp and nbr_sigma
    '''
    for i in range(nbr_samples):
        sample = list_of_n_randpixels(img_array, nbr_pix)

        if i == 0:
            dict_gmm = gmm_data_dict(sample, nbr_comp)

        else:
            gmm_2cpt = gmm_data_dict(sample, nbr_comp-1)
            means = gmm_2cpt['means']
            mu1 = max(means)
            mu2 = min(means)
            index = means.index(mu1)
            sigma1 = np.sqrt(gmm_2cpt['variances'][index])

            if test_dist_means(mu1, sigma1, mu2, nbr_sigma):
                dict_gmm = gmm_2cpt
            else:
                dict_gmm = gmm_data_dict(sample, nbr_comp)

        add_h0_dict(dict_gmm)
        dict_gmm['rf_observed'] = gmm_repartition_function(x, dict_gmm['means'], dict_gmm['variances'], dict_gmm['weights'])
        dict_gmm['rf_h0'] = gmm_repartition_function(x, dict_gmm['h0_means'], dict_gmm['h0_variances'], dict_gmm['h0_weights'])
        
        if gmm_data == dict():
            gmm_data = {pm: {page: {i: dict_gmm}}}
        elif pm not in gmm_data:
            gmm_data[pm] = {page: {i: dict_gmm}}
        elif page not in gmm_data[pm]:
            gmm_data[pm][page] = {i: dict_gmm}
        else:
            gmm_data[pm][page][i] = dict_gmm
    
    return gmm_data


def compute_pval(gmm_data, dict_pval):
    '''
    Dict[str, Dict[int, Dict[int, Dict[str, T]]]] * Dict[str, Tuple[int, float]] -> Dict[str, Tuple[int, float]]
    '''
    for pm, page in gmm_data.items():
        for num, iter in page.items():
            lst_delta = []

            for index, data in iter.items():
                if index == 0:
                    y0_ref = np.array(data['rf_h0'])
                    norm_ref = np.sum(np.abs(y0_ref - np.array(data['rf_observed'])))
                else:
                    y0 = np.array(data['rf_h0'])
                    delta_norm = np.sum(np.abs(y0_ref-y0))
                    lst_delta.append(delta_norm)

            pval = len([delta for delta in lst_delta if delta > norm_ref])/len(lst_delta)

        if dict_pval == dict():
            if pval < 0.05:
                dict_pval = {pm: [(num, pval, 'written')]}
            else:
                dict_pval = {pm: [(num, pval, 'blank')]}
        else:
            if pval < 0.05:
                dict_pval[pm].append((num, pval, 'written'))
            else:
                dict_pval[pm].append((num, pval, 'blank'))
    
    return dict_pval