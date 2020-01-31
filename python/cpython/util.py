"""
util.py: Utility functions to avoid boilerplate code

"""
import warnings


def dimension(dic=None, data=None):
    """ 
    Returns dimension of the data

    """
    if (dic is None) and (data is None):
        raise ValueError("Either data or dictionary must be supplied")

    elif dic is None:
            ndim = len(data.shape)

    elif data is None:
        if "acqus" in dic.keys():
            ndim = dic["acqus"]["PARMODE"] + 1
        else:
            ndim = 0
            for f in dic.keys():
                if f[:3] == "acq":
                    ndim += 1

    else:
        if verify(dic, data):
            ndim = dic["acqus"]["PARMODE"] + 1

    return ndim


def acqus_flist(dic, data, dim=None):
    """
    Returns a list of possible acqus files 
    that should be used for the data

    """
    if dim == None:
        dim = dimension(dic, data)

    return ["acuqs"] + [f"acqu{i}s" for i in range(2, dim + 1)]


def verify(dic, data, dtype="raw"):
    """ 
    Verifies that the size of data and the sizes
    mentioned in the dictionary are correct

    """
    verified = False

    acqus_files = acqus_flist(dic, data)
    points = [dic[f]["TD"] for f in acqus_files]

    expected_points = np.product(points) 
    actual_points = np.product(data.shape)

    if actual_points == expected_points:
        verified = True
    else:
        print(f"Actual Points {actual_points} do not match expected number "\
               "of points ({expected_points})")

    return verified


def fid_per_row(dic, data, direct_points=None, truncate_fids=None):
    """ 
    Returns a dataset as a 2D array with 
    one fid per row

    """
    v = verify(dic, data)

    if direct_points is None:
        try:
            direct_points = dic["acqus"]["TD"]
        except KeyError as e:
            raise KeyError("Cannot find number of points in the direct dimension")

    else:
        direct_points = int(direct_points)

    # first flatten the data to avoid some wierd bugs with the
    # way these data are stored
    data = data.reshape(-1)

    return data.reshape(-1, direct_points)


def split(dic, data, nsplits, stype="interleaved", td_per_split=None):
    """
    Splits data 
    
    """
    if verify(dic, data):
        data = fid_per_row(dic, data)
    else:
        raise ValueError("Inconsistent data")

    if stype in ["interleaved", "sequential"]:
        try:
            nsplits = int(insplits)
        except Exception:
            raise ValueError("nsplits must be integer")
        
    if stype == "interleaved":
        rem = data.shape[0] % nsplits
        if rem != 0:
            data = data[:-rem] 

    if stype == "sequential":
        if td_per_split is not None:
            td_per_split = int(t)

    if stype == "custom":
        try:
            nsplits = [int(i) for i in nsplits]
        except Exception:
            raise ValueError("nsplits must be a list of integers")

    if stype == "interleaved":
        return split_interleaved(data, nsplits)

    if stype == "sequential":
        return split_sequential(data, nsplits)

    if stype == "custom":
        return split_custom(data, nsplits)


def split_interleaved(data, nsplits):
    """
    Interleaved data splitting

    >>> import numpy as np
    >>> data = np.arange(50).reshape(5, 10)
    >>> from util import split_interleaved
    >>> data_split = split_interleaved(data, 2)
    >>> print(data_split[0])
    [[ 0  1  2  3  4  5  6  7  8  9]
     [20 21 22 23 24 25 26 27 28 29]
     [40 41 42 43 44 45 46 47 48 49]]
    >>> print(data_split[1])
    [[10 11 12 13 14 15 16 17 18 19]
     [30 31 32 33 34 35 36 37 38 39]]

    """
    if len(data.shape) != 2:
        raise ValueError("Needs 2D dataset. Must reshape before use")

    split_data = [data[i::nsplits] for i in range(nsplits)]

    return split_data


def split_sequential(data, nsplits, td_per_split=None):
    """
    Sequential data splitting

    >>> import numpy as np
    >>> from util import split_sequential
    >>> data = np.arange(100).reshape(10, 10)
    >>> d1 = split_sequential(data, 2)
    >>> d2 = split_sequential(data, 3, 3)
    >>> for i in d1:
    ...     print(i)
    [[ 0  1  2  3  4  5  6  7  8  9]
     [10 11 12 13 14 15 16 17 18 19]
     [20 21 22 23 24 25 26 27 28 29]
     [30 31 32 33 34 35 36 37 38 39]
     [40 41 42 43 44 45 46 47 48 49]]
    [[50 51 52 53 54 55 56 57 58 59]
     [60 61 62 63 64 65 66 67 68 69]
     [70 71 72 73 74 75 76 77 78 79]
     [80 81 82 83 84 85 86 87 88 89]
     [90 91 92 93 94 95 96 97 98 99]]
    >>> for i in d2:
    ...     print(i)
    [[ 0  1  2  3  4  5  6  7  8  9]
     [10 11 12 13 14 15 16 17 18 19]
     [20 21 22 23 24 25 26 27 28 29]]
    [[30 31 32 33 34 35 36 37 38 39]
     [40 41 42 43 44 45 46 47 48 49]
     [50 51 52 53 54 55 56 57 58 59]]
    [[60 61 62 63 64 65 66 67 68 69]
     [70 71 72 73 74 75 76 77 78 79]
     [80 81 82 83 84 85 86 87 88 89]]

    """
    if len(data.shape) != 2:
        raise ValueError("Needs 2D dataset. Must reshape before use")

    if td_per_split is None:
        res = data.shape[0] % nsplits  
        if res == 0:
            l = data.shape[0] // nsplits
        else:
            data = data[0:-res]
            l = data.shape[0] // nsplits

    else:
        l = td_per_split

    split_data = [data[i*l : (i+1)*l] for i in range(nsplits)]

    return split_data


def split_custom(data, nsplits):
    """
    Split custom data
    >>> import numpy as np
    >>> from util import split_custom
    >>> data = np.arange(100).reshape(10, 10)
    >>> d1 = split_custom(data, [0, 3, 7])
    >>> for i in d1:
    ...     print(i)
    [0 1 2 3 4 5 6 7 8 9]
    [30 31 32 33 34 35 36 37 38 39]
    [70 71 72 73 74 75 76 77 78 79]

    """
    if len(data.shape) != 2:
        raise ValueError("Needs 2D dataset. Must reshape before use")

    split_data = [data[i] for i in nsplits]

    return split_data


def rectify_increments(dic, data, dim, td):
    """ Changes the number of points in the """


def protect_overwriting(dir_list, subdir_list=None):
    """ check whether a directory/file exists """

    for dirc in dir_list:
        if subdir_list is not None:
            for f in subdir_list:
                if os.path.exists(os.path.join(dirc, str(f))):
                    raise ValueError(f"Directory/File {dirc}/{file} exists")
        else:
            if os.path.exists(dirc):
                raise ValueError(f"Directory/File {dirc}/{file} exists")

    return True
