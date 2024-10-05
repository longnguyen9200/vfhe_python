from imports import *
from random_poly_ring import *
from scheme_bgv import gen_public_key

def poly_to_base_list(poly: quotient_ring_poly, base: int):
    col = math.ceil(math.log(poly.coef_modulus, base))
    row = len(poly.poly_modulus)-1
    coefs = np.zeros((row, col), dtype=object)
    result = []
    for i in range(len(poly.coef_poly)):
        coef = poly.coef_poly[i]
        a = int_to_base_list(coef%poly.coef_modulus,base)
        addition_slot = col - len(a)

        a = np.pad(a, (0,addition_slot))
        coefs[i] = a 
    for i in range(col):
        p = quotient_ring_poly(coefs[:,i], poly.coef_modulus,poly.poly_modulus)
        result.append(p)
    return result

def gen_relin_key(
        secret_key: quotient_ring_poly,
          base: int, coef_modulus:int,
          poly_modulus:quotient_ring_poly,
          plaintext_modulus:int ):
    terms = math.ceil(math.log(coef_modulus, base))
    evaluation_keys =[]
    for i in range(terms):
        b, a = gen_public_key(secret_key,coef_modulus,poly_modulus,plaintext_modulus)
        ek0 = b + secret_key*secret_key * base**i
        ek1 = a
        evaluation_keys.append((ek0,ek1))
    return evaluation_keys

def rerelinearization(
        ciphertext_0:quotient_ring_poly,
        ciphertext_1:quotient_ring_poly,
        ciphertext_2:quotient_ring_poly,
        evaluation_keys,
        base:int,
        coef_modulus:quotient_ring_poly,
        poly_modulus:quotient_ring_poly):
    ciphertext_2_poly = poly_to_base_list(ciphertext_2,base)
    ciphertext_0_relin = ciphertext_0
    ciphertext_1_relin = ciphertext_1
    for c2,(ek0,ek1) in zip(ciphertext_2_poly, evaluation_keys):
        ciphertext_0_relin += c2*ek0
        ciphertext_1_relin += c2*ek1
    return ciphertext_0_relin,ciphertext_1_relin

