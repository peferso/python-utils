from numpy import array, unique, eye, zeros, vstack, sum, matmul, nan


def one_hot(
    array: array
):
    _unique, inverse = unique(array, return_inverse=True)
    onehot = eye(_unique.shape[0])[inverse]
    return (onehot, _unique)


def base_vector(i, dim):
    v = zeros(dim)
    v[i] = 1
    return v


def filter_by_elements(
    ohsarray: array,
    elements: array,
    correspondence: dict
):
    n = elements.shape[0]
    f = correspondence[elements[0]]
    if n > 1:
        for i in range(1, n):
            v = correspondence[elements[i]]
            f = vstack((f, v))
    mult = matmul(ohsarray, f.T)
    if n > 1:
        mult = sum(mult, axis=1)
    return mult == 1


def numpy_isin(
    column_array: array,
    filtering_list: list
):
    if len(filtering_list) == 0:
        return array([nan]*(column_array.shape[0]))
    strarray = array(column_array).astype(str)
    ohsarray, _unique = one_hot(strarray)
    correspondence = {
        _unique[i]: base_vector(i, _unique.shape[0])
        for i in range(_unique.shape[0])
    }
    elements = array(filtering_list)
    filter = filter_by_elements(
        ohsarray,
        elements,
        correspondence
    )
    column_array[~filter] = nan
    return column_array
