from imports import *
def random_sk_poly(coef_modulus:int, poly_modulus:np.array):
    size = len(poly_modulus)-1
    result_poly = np.random.choice(np.array([-1,0,1]),size=size, p=[1/4,1/2,1/4])
    return quotient_ring_poly(result_poly,coef_modulus, poly_modulus)

def random_uniform_poly(coef_modulus:int, poly_modulus:np.array, plaintext_modulus=None):
    if plaintext_modulus == None:
        plaintext_modulus = coef_modulus -1
    size = len(poly_modulus) - 1
    result_poly = np.array([random.randrange(0, plaintext_modulus) for _ in range(size)])
    return quotient_ring_poly(result_poly, coef_modulus,poly_modulus)

def random_normal_poly(coef_modulus:int, poly_modulus:np.array):
    size = len(poly_modulus)-1
    mu, sigma = 0, 3.8
    result_poly = np.random.normal(loc=mu, scale=sigma, size=size)
    result_poly = np.round(result_poly)
    return quotient_ring_poly(result_poly, coef_modulus,poly_modulus)

    # poly_modulus = init_poly_modulus(poly_modulus)
    # size = len(poly_modulus) - 1
    # coef = np.array([round(random.gauss(mu, sigma)) for _ in range(size)], dtype=object)
    # return quotient_ring_poly(coef, coef_modulus, poly_modulus)
