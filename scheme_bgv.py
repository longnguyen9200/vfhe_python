from imports import *
from random_poly_ring import *

def gen_secret_key(coef_modulus:int, poly_modulus:np.array):
    sk = random_sk_poly(coef_modulus,poly_modulus);
    return sk

def gen_public_key(secret_key:quotient_ring_poly,coef_modulus:int, poly_modulus:np.array, plaintext_modulus: int):
    error_poly= random_normal_poly(coef_modulus,poly_modulus)
    a = random_uniform_poly(coef_modulus,poly_modulus)
    public_key_0 = a * secret_key + error_poly * plaintext_modulus
    public_key_1 = -a
    return public_key_0,public_key_1

def encryptor(
  message: quotient_ring_poly,
  public_key_0:quotient_ring_poly,
  public_key_1:quotient_ring_poly,
  coef_modulus: int,
  poly_modulus: np.array,
  plaintext_modulus:int   
):
    error_poly_0 = random_normal_poly(coef_modulus, poly_modulus)
    error_poly_1 = random_normal_poly(coef_modulus,poly_modulus)

    u = random_sk_poly(coef_modulus,poly_modulus)

    ciphertext_0 = public_key_0*u + error_poly_0 * plaintext_modulus+ message
    ciphertext_1 = public_key_1*u+ error_poly_1 * plaintext_modulus
    return ciphertext_0,ciphertext_1

def decryptor(
    ciphertext_0: quotient_ring_poly,
    ciphertext_1:quotient_ring_poly,
    secret_key:quotient_ring_poly,
    plaintext_modulus:int,
    noise:False
):
    message = ciphertext_0+ciphertext_1*secret_key
    message = message % plaintext_modulus
    noise = np.max(np.abs(message.coef_poly))
    if noise:
        return message,noise
    return message

def add(ciphertext_0,ciphertext_1, ciphertext_0_, ciphertext_1_):
    return ciphertext_0+ciphertext_0_, ciphertext_1+ciphertext_1_

def mul(ciphertext_0,ciphertext_1, ciphertext_0_, ciphertext_1_):
    return ciphertext_0*ciphertext_0_, ciphertext_0*ciphertext_1_+ciphertext_1*ciphertext_0_,ciphertext_1*ciphertext_1_

def mul_mess(ciphertext_0,ciphertext_1, ciphertext_2, secret_key, plaintext_modulus, noise:False):
    messages_result = ciphertext_0+ciphertext_1*secret_key+ciphertext_2*secret_key*secret_key
    noise = np.max(np.abs(messages_result.coef_poly))

    messages_result%=plaintext_modulus
    if noise:
        return messages_result, noise
    return messages_result
