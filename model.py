from imports import *
from number_untils import *
from quotient_ring import *
from random_poly_ring import *
from scheme_bgv import *
from ascii_trans import *
from key_switching import *
from read_csv import *
from cryptoFile_exporter import *
from export_csv import *

class DataModel:
    def __init__(self):
        self.selected_option = None
        self.file_path = None
        self.n_number = None
        self.coef_modulus = None
        self.poly_modulus = None
        self.plaintext_modulus = None
        self.base = None
        self.c0_path =None
        self.c1_path =None
        self.sk =None

    def set_selected_option(self, option):
        self.selected_option = option

    def set_file_path(self, file_path):
        self.file_path = file_path

    def set_value(self,n_number, plaintext_modulus, base):
        self.n_number = n_number
        self.coef_modulus = getRandomNBitInteger(128)
        self.poly_modulus = init_poly_modulus(n_number)
        self.plaintext_modulus = plaintext_modulus
        self.base = base

    def set_decrypt_value(self,c0_path,c1_path,sk_path, plaintext_modulus):
        self.c0_path = c0_path
        self.c1_path =c1_path
        self.sk = read_sk_from_file(sk_path)
        self.plaintext_modulus =plaintext_modulus

    def get_selected_option(self):
        return self.selected_option

    def get_file_path(self):
        return self.file_path

    def get_n_number(self):
        return self.n_number

    def get_coef_modulus(self):
        return self.coef_modulus

    def get_poly_modulus(self):
        return self.poly_modulus

    def get_plaintext_modulus(self):
        return self.plaintext_modulus

    def get_base(self):
        return self.base
    
    def get_c0_path(self):
        return self.c0_path
    
    def get_c1_path(self):
        return self.c0_path    
    
class EncryptionService:
    def __init__(self):
        pass
    
    def process_encyption(self,data):
        n = data['n_number']
        
        # Gen Key
        secret_key = gen_secret_key(data['coef_modulus'], data['poly_modulus'])
        print('sk:',secret_key)
        public_key_0, public_key_1 = gen_public_key(secret_key,data['coef_modulus'],data['poly_modulus'],data['plaintext_modulus'])
        eks = gen_relin_key(secret_key,data['base'],data['coef_modulus'],data['poly_modulus'], data['plaintext_modulus'])

        print("public_key_0:",public_key_0)
        print("public_key1",public_key_1)
        print("eks",eks)
        name_and_gender,income,tax,vat,environmental_protection_tax,parm = read_csv_data(data["file_path"])
        name_gender_acsii =[]
        name_and_gender_poly =[]
        result_income = []

        name_and_gender,incomes,taxs,vats,environmental_protection_taxs,parms = read_csv_data(data['file_path'])

        for item in name_and_gender:
            name_gender_acsii.append(string_to_ascii_array(item))
            plaintext = quotient_ring_poly(string_to_ascii_array(item),data['coef_modulus'],data['poly_modulus'])
            name_and_gender_poly.append(plaintext)
            (c0,c1) = encryptor(plaintext,public_key_0,public_key_1,data['coef_modulus'], data['poly_modulus'], data['plaintext_modulus'])
            result_income.append((c0,c1))
        
        for income,tax,vat,env_tax, parm in zip(incomes,taxs,vats,environmental_protection_taxs,parms):
            income_plaintext = quotient_ring_poly([income],data['coef_modulus'],data['poly_modulus'])
            tax_plaintext = quotient_ring_poly([-tax],data['coef_modulus'],data['poly_modulus'])
            vat_plaintext = quotient_ring_poly([-vat],data['coef_modulus'],data['poly_modulus'])
            env_plaintext = quotient_ring_poly([-env_tax],data['coef_modulus'],data['poly_modulus'])
            parm_plaintext = quotient_ring_poly([parm],data['coef_modulus'],data['poly_modulus'])

            c0,c1 = encryptor(income_plaintext,public_key_0,public_key_1,data['coef_modulus'],data['poly_modulus'],data['plaintext_modulus'])
            c0_,c1_ = encryptor(tax_plaintext,public_key_0,public_key_1,data['coef_modulus'],data['poly_modulus'],data['plaintext_modulus'])
            c0_res,c1_res = add(c0,c1,c0_,c1_)
            c0_,c1_ = encryptor(vat_plaintext,public_key_0,public_key_1,data['coef_modulus'],data['poly_modulus'],data['plaintext_modulus'])
            c0_res,c1_res = add(c0_res,c1_res,c0_,c1_)

            c0,c1 = encryptor(env_plaintext,public_key_0,public_key_1,data['coef_modulus'],data['poly_modulus'],data['plaintext_modulus'])
            c0_,c1_ = encryptor(parm_plaintext,public_key_0,public_key_1,data['coef_modulus'],data['poly_modulus'],data['plaintext_modulus'])
            c0_mul,c1_mul,c2_mul = mul(c0,c1,c0_,c1_)
            c0_hat, c1_hat = rerelinearization(c0_mul,c1_mul,c2_mul,eks,data['base'],data['coef_modulus'],data['poly_modulus'])

            c0_res,c1_res = add(c0_res,c1_res,c0_hat,c1_hat)
            result_income.append((c0_res,c1_res))

        write_list_to_file(result_income,"./ciphertext/c0.txt","./ciphertext/c1.txt")
        write_sk_to_file(secret_key,"./ciphertext/sk.txt")
        print("Encrypt success")


class DecryptionService:
    def __init__(self):
        pass       

    def process_decryption(self,data):

        ciphertext_from_file =read_file_to_list(data['c0_path'],data['c1_path'])
        mid_index = len(ciphertext_from_file)//2
        name_and_gen_ascii =[]
        name_and_gen =[]
        incomes =[]
        for item in ciphertext_from_file[:mid_index]:
            c0_file = item[0][0]
            c1_file = item[1][0]
            poly_modulus = np.array(item[0][2],dtype=object)
            message, noise_val = decryptor(quotient_ring_poly(c0_file,item[0][1],poly_modulus),quotient_ring_poly(c1_file,item[0][1],poly_modulus),data['sk'],data['plaintext_modulus'],noise=True)
            name_and_gen_ascii.append(message)
        for item in name_and_gen_ascii:
            name_gender= ascii_array_to_string(item.coef_poly)
            name_gender = name_gender.replace('\x00', '')
            name_and_gen.append(name_gender)

        for item in ciphertext_from_file[mid_index:]:
            c0_file = item[0][0]
            c1_file = item[1][0]
            poly_modulus = np.array(item[0][2],dtype=object)
            income, noise_val = decryptor(quotient_ring_poly(c0_file,item[0][1],poly_modulus),quotient_ring_poly(c1_file,item[0][1],poly_modulus),data['sk'],data['plaintext_modulus'],noise=True)
            incomes.append(income.coef_poly[0])   

        data_to_csv =[]
        data_to_csv.append(["Name","Gender","Income"])
        for name_gen,income in zip(name_and_gen,incomes):
            data_to_csv.append([name_gen[:-1],"Male" if name_gen[-1] == "0" else "Female",income])
        for item in data_to_csv:
            print(item)
        write_data_to_csv(data_to_csv,"./message/business_revenue_table.csv")