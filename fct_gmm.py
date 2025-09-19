import numpy as np
from itertools import chain
from scipy.special import erf
from sklearn.mixture import GaussianMixture
from fct_h0 import get_h0



def get_gmm(sample, nbr_comp):
    '''
    List[int] * int -> GaussianMixture
    '''
    x = np.asarray(sample)
    x = x.reshape(-1,1)
    return GaussianMixture(n_components=nbr_comp).fit(x)


def get_means_lst_gmm(gmm):
    '''
    GaussianMixture -> List[float]
    '''
    return list(chain.from_iterable((gmm.means_).tolist()))


def get_variances_lst_gmm(gmm):
    '''
    GaussianMixture -> List[float]
    '''
    return list(chain.from_iterable(chain.from_iterable((gmm.covariances_).tolist())))


def get_weights_lst_gmm(gmm):
    '''
    GaussianMixture -> List[float]
    '''
    return (gmm.weights_).tolist()


def gmm_data_dict(sample, nbr_comp):
    '''
    List[Tuple[str, List[int]]] * int -> Dict[str, Dict[int, Dict[str, T]]]
    '''
    gmm = get_gmm(sample, nbr_comp)
    means = get_means_lst_gmm(gmm)
    vars = get_variances_lst_gmm(gmm)
    weights = get_weights_lst_gmm(gmm)

    return {'n_components': gmm.n_components,
            'means': means,
            'variances': vars,
            'weights': weights}


def normal_repartition_function(x, mu, sigma, weight):
    '''
    List[int] * float * float * float -> List[float]
    '''
    return [float(0.5*(1+erf((x_i-mu)/(sigma*np.sqrt(2))))*weight) for x_i in x]
    

def gmm_repartition_function(x, means, vars, weights):
    '''
    List[int] * List[float] * List[float] * List[float] -> List[float]
    '''
    rfs_comp = [normal_repartition_function(x, mean, np.sqrt(var), weight) for mean, var, weight in zip(means, vars, weights)]
    y_rf_gmm = []
    for i in range(len(rfs_comp)):
        if i == 0:
            y_rf_gmm = rfs_comp[i]
        else:
            y_rf_gmm = list(map(lambda x,y: x+y, y_rf_gmm, rfs_comp[i]))
    return y_rf_gmm


def add_fct_repartiton(x, data_gmm, index):
    '''
    np.1darray * Dict[str, Dict[int, Dict[str, T]]] -> None
    '''
    for _, data in data_gmm.items():
        data[index]['y_rf_gmm'] = gmm_repartition_function(x, data[index]['means'],
                                                           data[index]['variances'],
                                                           data[index]['weights'])
        data[index]['y_rf_h0'] = gmm_repartition_function(x, data[index]['h0_means'],
                                                          data[index]['h0_variances'],
                                                          data[index]['h0_weights'])