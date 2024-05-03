from imports import *
from number_untils import *
def polydiv(poly1, poly2):
    while len(poly1) >= len(poly2):
        quotient = poly1[-1] // poly2[-1]
        res = np.zeros(len(poly1), dtype=object)
        res[-len(poly2) :] = quotient * poly2

        sub = poly1 - res

        while len(sub) > 0 and sub[-1] == 0:
            sub = sub[:-1]

        poly1 = sub

    quotient = np.zeros(len(poly1) + len(poly2) - 1, dtype=object)
    quotient[-len(poly1) :] = poly1
    remainder = poly1
    return quotient, remainder