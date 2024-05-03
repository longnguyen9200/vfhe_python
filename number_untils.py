
from imports import *

def round_coef(array):
    return np.array([round(a) for a in array],dtype=object)


def int_coef(array):
    return np.array([int(a) for a in array],dtype=object)


def int_to_base_list(x: int, base: int) -> List[int]:
    result = []
    while x > 0:
        q, r = divmod(x, base)
        result.append(r)
        x = q
    return result

def mod_center(x, m: int, left: bool = True):
    if left:
        return (x + m // 2) % m - m // 2
    else:
        return (x + m // 2 - 1) % m - m // 2 + 1