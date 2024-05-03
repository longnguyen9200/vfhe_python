from imports import *
def modulus_switching(poly: quotient_ring_poly,Q:int,p:int, plaintext_modulus:int):
    if Q % p != 0:
        raise ValueError("big_mod must be divisible by small_mod")

    delta = Q//p

    d = ((-poly * pow(plaintext_modulus, -1, delta)) % delta) * plaintext_modulus

    if d % delta != (-poly % delta):
        raise ValueError("Adjustment term d is not computed correctly")

    if not all((d % plaintext_modulus).coef_poly == 0):
        raise ValueError("All coefficients of d must be 0 modulo plaintext_modulus")
    
    switched_poly = (d+poly) *(p/Q)

    if not all(poly.coef_poly % plaintext_modulus == switched_poly.coef_poly % plaintext_modulus):
        raise ValueError("Coefficients of x_ do not match coefficients of x modulo plaintext_modulus")
    
    return switched_poly
