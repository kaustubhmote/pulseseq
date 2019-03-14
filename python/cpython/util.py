"""
util.py: Utility functions to avoid boilerplate code

"""
import warnings


def dimension(dic=None, data=None):
    """ dimension of the
    """
    if dic == data == None:
        raise ValueError('Either data or dictionary must be supplied')

    if 'acqus' in dic.keys():
        return dic['acqus']['PARMODE'] + 1
    else:
        ndim = 0
        for f in dic.keys():
            if f[:3] == 'acq':
                ndim += 1
        if ndim > 0:
            return ndim
        else:
            return len(data.shape)        


def acqus_flist(dic, data, dim=None):
    """returns a list of possible acqus files 
    that should be used for the data
    """
    if dim == None:
        dim = dimension(dic, data)

    return ['acuqs'] + ['acqu{}s'.format(i) for i in range(2, dim+1)]


def verify(dic, data):
    """ verifies that the size of data and the sizes
    mentioned in the dictionary are correct
    """


def fid_per_row(dic, data, direct_points=None, truncate_fids=None):
    """ returns a dataset as a 2D array with 
    one fid per row
    """

    if direct_points == None:
        try:
            direct_points = dic['acqus']['TD']
        except KeyError:
            warn('Cannot reshape the data. Check your dictionary or 
                  manually give the number of points in direct dimension')
    else: 
        direct_points = int(direct_points)

    # first flatten the data to avoid some wierd bugs with the 
    # way these data are stored
    data = data.reshape(-1)
    return data.reshape(-1, direct_points)


def split(dic, data, num_split, type='interleaved'):
    """ Splits data """


def rectify_increments(dic, data, dim, td):
    """ Changes the number of points in the """


def protect_overwriting(dir_list, subdir_list=None):
    """ check whether a directory/file exists """

    for dirc in dir_list:
        for f in subdir_list:
            if os.path.exists(os.path.join(dirc, f)):
               raise ValueError(f'Directory/File {dirc}/{file} exists') 

    return 


