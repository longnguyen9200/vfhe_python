import ast
from quotient_ring import *
def write_list_to_file(list_items, file_name_c0, file_name_c1):
    with open(file_name_c0, 'w', encoding='utf-8') as file:
        for item in list_items:
            poly1,_ = item
            coef_poly1_str = ', '.join(map(str, poly1.coef_poly))
            coef_modulus1_str = str(poly1.coef_modulus)
            poly_modulus1_str = ', '.join(map(str, poly1.poly_modulus))
            file.write(f"([{coef_poly1_str}], {coef_modulus1_str}, [{poly_modulus1_str}])\n")
            
    with open(file_name_c1,'w',encoding='utf-8') as file:
        for item in list_items:
            _, poly2 = item
            coef_poly2_str = ', '.join(map(str, poly2.coef_poly))
            coef_modulus2_str = str(poly2.coef_modulus)
            poly_modulus2_str = ', '.join(map(str, poly2.poly_modulus))
            file.write(f"([{coef_poly2_str}], {coef_modulus2_str}, [{poly_modulus2_str}])\n")

def read_file_to_list(file_name1,file_name2):
    # list_items = []
    # with open(file_name1, 'r', encoding='utf-8') as file:
    #     for line in file:
    #         item = ast.literal_eval(line.strip())
    #         list_items.append(item)
    with open(file_name1, 'r') as file1, open(file_name2, 'r') as file2:
        
        lines_a = file1.readlines()
        lines_b = file2.readlines()

    
    item_list = []
    for line_a, line_b in zip(lines_a, lines_b):
        
        item = (ast.literal_eval(line_a.strip()),ast.literal_eval(line_b.strip()))
        item_list.append(item)

    return item_list

def write_sk_to_file(sk,file_name):
    with open(file_name, 'w', encoding='utf-8') as file:
            coef_poly_str = ', '.join(map(str, sk.coef_poly))
            coef_modulus_str = str(sk.coef_modulus)
            poly_modulus_str = ', '.join(map(str, sk.poly_modulus))
            file.write(f"([{coef_poly_str}], {coef_modulus_str}, [{poly_modulus_str}])\n")

def read_sk_from_file(file_path):
    with open(file_path,'r') as file:
        line = file.readline()
        item = ast.literal_eval(line.strip())
        return quotient_ring_poly(item[0], item[1],item[2])

# a = read_sk_from_file('./ciphertext/sk.txt')
# print(a.coef_poly)