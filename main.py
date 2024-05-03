
from imports import *
from number_untils import *
from quotient_ring import *
from random_poly_ring import *
from scheme_bgv import *
from ascii_trans import *
from key_switching import *
from read_csv import *
from cryptoFile_exporter import *

n= 2**5 #2^5
coef_modulus = getRandomNBitInteger(128)
poly_modulus = init_poly_modulus(n)
plaintext_modulus = 10000  #1000
base = 5

sk = gen_secret_key(coef_modulus,poly_modulus)
print("secret_key:  ",type(sk))
pk0,pk1= gen_public_key(sk,coef_modulus,poly_modulus,plaintext_modulus)

eks = gen_relin_key(sk,base,coef_modulus,poly_modulus,plaintext_modulus)

# print(eks)

# # encrypt 1 mess
# msg = random_uniform_poly(coef_modulus,poly_modulus,plaintext_modulus)
# msg.coef_poly = string_to_ascii_array("nguyen thang long")


# c0,c1= encryptor(msg,pk0,pk1,coef_modulus,poly_modulus,plaintext_modulus)

# decr_msg, noise_val = decryptor(c0,c1,sk,plaintext_modulus, noise =True)
# print(decr_msg.coef_poly)
# print(msg.coef_poly)
# print("noise:", noise_val<coef_modulus/2)
# message = ascii_array_to_string(decr_msg.coef_poly)
# print(message)


# encrypt 2 mess and caculation
# mes_1 = random_uniform_poly(coef_modulus, poly_modulus, plaintext_modulus)
# mes_2 = random_uniform_poly(coef_modulus,poly_modulus,plaintext_modulus)
# mes_1 = quotient_ring_poly([4000], coef_modulus,poly_modulus)
# mes_2 = quotient_ring_poly([2],coef_modulus,poly_modulus)

# (c0,c1)= encryptor(mes_1,pk0,pk1,coef_modulus,poly_modulus,plaintext_modulus)
# (c0_,c1_)= encryptor(mes_2,pk0,pk1,coef_modulus,poly_modulus,plaintext_modulus)

# result = (mes_1 * mes_2) % plaintext_modulus

# c0_res, c1_res, c2_res = mul(c0,c1,c0_,c1_)
# mul_mess_, noise_= mul_mess(c0_res,c1_res,c2_res,sk,plaintext_modulus,noise=True)

# c0_hat, c1_hat = rerelinearization(c0_res,c1_res,c2_res,eks,base,coef_modulus,poly_modulus)
# # print("co is: ",c0_hat,"\n","c1 is:",c1_hat)
# mes_decryp, noise_val = decryptor(c0_hat,c1_hat,sk,plaintext_modulus,noise=True)

# print("mess 1:",mes_1)
# print("mess 2:", mes_2)
# print ("c0_hat:",c0_hat)
# print("c1_hat:",c1_hat)

# print("Reliniarization decr", mes_decryp.coef_poly.astype(int))
# print("Quadratic decryption", mul_mess_.coef_poly.astype(int))
# print("Real result         ", result.coef_poly.astype(int))
# print("noise in norrmal caculator:",noise_,"\n","noise in relinearization:", noise_val,"\n", "max noise:",coef_modulus//2)



# Main
name_gender_ascii =[]
name_and_gender_poly =[]
name_and_gender_ecrypt =[]
result_income = []

name_and_gender_decrypt =[]
ciphertext_from_file =[]
name_and_gender_ascii_before_decrypt=[]
name_and_gender_ascii_to_plaintext =[]
name_and_gender,incomes,taxs,vats,environmental_protection_taxs,parms = read_csv_data('./database/100_employeers.csv')

for name_gender in name_and_gender:
    name_gender_ascii.append(string_to_ascii_array(name_gender))
    msg = quotient_ring_poly(string_to_ascii_array(name_gender),coef_modulus,poly_modulus)
    name_and_gender_poly.append(msg)
    (c0,c1)= encryptor(msg,pk0,pk1,coef_modulus,poly_modulus,plaintext_modulus)
    result_income.append((c0,c1))



for income,tax,vat,env_tax, parm in zip(incomes,taxs,vats,environmental_protection_taxs,parms):
    income_plaintext = quotient_ring_poly([income],coef_modulus,poly_modulus)
    tax_plaintext = quotient_ring_poly([-tax],coef_modulus,poly_modulus)
    vat_plaintext = quotient_ring_poly([-vat],coef_modulus,poly_modulus)
    env_plaintext = quotient_ring_poly([-env_tax],coef_modulus,poly_modulus)
    parm_plaintext = quotient_ring_poly([parm],coef_modulus,poly_modulus)
    
    c0,c1 = encryptor(income_plaintext,pk0,pk1,coef_modulus,poly_modulus,plaintext_modulus)
    c0_,c1_ = encryptor(tax_plaintext,pk0,pk1,coef_modulus,poly_modulus,plaintext_modulus)
    c0_res,c1_res = add(c0,c1,c0_,c1_)
    c0_,c1_ = encryptor(vat_plaintext,pk0,pk1,coef_modulus,poly_modulus,plaintext_modulus)
    c0_res,c1_res = add(c0_res,c1_res,c0_,c1_)

    c0,c1 = encryptor(env_plaintext,pk0,pk1,coef_modulus,poly_modulus,plaintext_modulus)
    c0_,c1_ = encryptor(parm_plaintext,pk0,pk1,coef_modulus,poly_modulus,plaintext_modulus)
    c0_mul,c1_mul,c2_mul = mul(c0,c1,c0_,c1_)
    c0_hat, c1_hat = rerelinearization(c0_mul,c1_mul,c2_mul,eks,base,coef_modulus,poly_modulus)

    c0_res,c1_res = add(c0_res,c1_res,c0_hat,c1_hat)
    result_income.append((c0_res,c1_res))

write_list_to_file(result_income,"./ciphertext/c0.txt","./ciphertext/c1.txt")
write_sk_to_file(sk,"./ciphertext/sk.txt")
secret_key = read_sk_from_file("./ciphertext/sk.txt")
# print(read_sk_from_file("./ciphertext/sk.txt"))
ciphertext_from_file = read_file_to_list("./ciphertext/c0.txt","./ciphertext/c1.txt")
# print(len(ciphertext_from_file))
mid_index = len(ciphertext_from_file)//2
for item in ciphertext_from_file[:mid_index]:
    c0_file = item[0][0]
    c1_file = item[1][0]
    message, noise_val = decryptor(quotient_ring_poly(c0_file, coef_modulus,item[0][2]),quotient_ring_poly(c1_file,coef_modulus,poly_modulus),secret_key,plaintext_modulus,noise=True)
    name_and_gender_ascii_before_decrypt.append(message)
for item in name_and_gender_ascii_before_decrypt:
    name_gender= ascii_array_to_string(item.coef_poly)
    name_and_gender_ascii_to_plaintext.append(name_gender)

for item in name_and_gender_ascii_to_plaintext:
    print(item)

for item in ciphertext_from_file[mid_index:]:
    c0_file = item[0][0]
    c1_file = item[1][0]
    message, noise_val = decryptor(quotient_ring_poly(c0_file, coef_modulus,poly_modulus),quotient_ring_poly(c1_file,coef_modulus,poly_modulus),sk,plaintext_modulus,noise=True)
    print(message)

# for item in ciphertext_from_file:
#     c0_file = item[0][0]
#     c1_file = item[1][0]
#     message, noise_val = decryptor(quotient_ring_poly(c0_file, coef_modulus,poly_modulus),quotient_ring_poly(c1_file,coef_modulus,poly_modulus),sk,plaintext_modulus,noise=True)
#     name_and_gender_ascii_before_decrypt.append(message)
# for item in name_and_gender_ascii_before_decrypt:
#     name_gender= ascii_array_to_string(item.coef_poly)
#     name_and_gender_ascii_to_plaintext.append(name_gender)

# # for item in name_and_gender_ascii_to_plaintext:
# #     print(item)



# income_encrypt = quotient_ring_poly([income[0]],coef_modulus,poly_modulus)
# (c0,c1)= encryptor(income_encrypt,pk0,pk1,coef_modulus,poly_modulus,plaintext_modulus)
# print(income_encrypt)
# parm_encrypt = quotient_ring_poly([parm[0]],coef_modulus,poly_modulus)
# (c0_,c1_) = encryptor(parm_encrypt,pk0,pk1,coef_modulus,poly_modulus,plaintext_modulus)
# print(parm_encrypt)

# c0_res, c1_res, c2_res = mul(c0,c1,c0_,c1_)
# c0_hat, c1_hat = rerelinearization(c0_res,c1_res,c2_res,eks,base,coef_modulus,poly_modulus)
# mes_decrypt, noise_val = decryptor(c0_hat,c1_hat,sk,plaintext_modulus,noise=True)

# print(mes_decrypt.coef_poly)



