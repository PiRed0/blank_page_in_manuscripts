from random import seed, randint


# initialization of the generator of random numbers
seed()


def rand2Dcoord(x_max, y_max):
    '''
    int * int -> Tuple[int, int]
    Returns 2D coordinates randomly generated
    x <= x_max and y <= y_max
    '''
    return randint(0, x_max), randint(0, y_max)


def list_rand2Dcoord(x_max, y_max, nbr_iter):
    '''
    int * int *int -> List[Tuple[int, int]]
    Returns a list of nbr_inter long of 2D coordinates
    randomly generated with: x <= x_max and y <= y_max
    '''
    lst_randcoord = []
    for i in range(nbr_iter):
        lst_randcoord.append(rand2Dcoord(x_max, y_max))
    return lst_randcoord


def list_randpixels(img_array, lst_randcoord):
    '''
    np.2darray * List[Tuple[int, int]] -> List[int]
    Require: img_array is an array of a grayscale image
    Returns a list of random pixels from img_array
    given the lsit of random coordiantes lst_randcoord
    '''
    lst_randpix = []
    for x, y in lst_randcoord:
        lst_randpix.append(int(img_array[x,y]))
    return lst_randpix


def list_of_n_randpixels(img_array, nbr_pix):
    '''
    np.2darray * int -> List[int]
    Require: nbr_pix >= 0
    Returns a list of nbr_pix long ofrandom pixels
    from img_array
    '''
    height = img_array.shape[0]
    width = img_array.shape[1]
    lst_randcoord = list_rand2Dcoord(x_max=(height-1), y_max=(width-1), nbr_iter=nbr_pix)
    return list_randpixels(img_array, lst_randcoord)