import numpy as np



def get_h0(means, vars, weights):
    '''
    List[float] * List[float] * List[float] ->
    List[float] * List[float] * List[float]
    '''
    if len(means) > 2:
        h0_means = list(means)
        h0_vars = list(vars)
        h0_weights = list(weights)

        i = h0_means.index(min(h0_means))

        h0_means.pop(i)
        h0_vars.pop(i)
        h0_weights.pop(i)

        sum_weights = np.sum(h0_weights)
        h0_weights = [float(w / sum_weights) for w in h0_weights]

        return h0_means, h0_vars, h0_weights
    
    return means, vars, weights


def add_h0_dict(dict_gmm):
    '''
    Dict[str, T] -> None
    '''
    h0_means, h0_vars, h0_weights = get_h0(dict_gmm['means'], dict_gmm['variances'], dict_gmm['weights'])
    dict_gmm['h0_means'] = h0_means
    dict_gmm['h0_variances'] = h0_vars
    dict_gmm['h0_weights'] = h0_weights


def distance_h0_observed(y_h0, y_observed):
    '''
    List[float] * List[float] -> float
    '''
    delta_max = 0.0
    for y0, y1 in zip(y_h0, y_observed):
        delta = float(np.abs(y1-y0))
        if delta > delta_max:
            delta_max = delta
    return delta_max


def add_infinite_norm(data_gmm, index):
    '''
    Dict[str, Dict[int, Dict[str, T]]] -> None
    '''
    for _, data in data_gmm.items():
        data[index]['distance_h0'] = distance_h0_observed(data[index]['y_rf_gmm'], data[index]['y_rf_h0'])


def test_dist_means(mu1, sigma1, mu2, nbr_sigma):
    '''
    Precondition: mu1 > mu2
    float * float * float -> True
    '''
    return mu1 - sigma1 * nbr_sigma < mu2