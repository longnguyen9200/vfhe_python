import csv
import pandas as pd

def read_csv_data(file_path):
    personal_info = []
    income= []
    tax=[]
    vat=[]
    environmental_protection_tax=[]
    parm=[]
    data = pd.read_csv(file_path)
    data
    for index,row in data.iterrows():
        full_name_gender = (row["first_name"]+" "+row["last_name"]).lower()+("0" if row["gender"].lower() == "male" else "1")
        personal_info.append(full_name_gender)
        
        # weight = float(row["weight"])
        # weight_int = int(weight)
        # weight_dec= (weight-weight_int)*10
        # height_weight.append((int(row["height"]),weight_int, int(weight_dec)))
        income.append(int(row["aggregate_income"]))
        tax.append(int(row["tax"]))
        vat.append(int(row["vat"]))
        environmental_protection_tax.append(int(row["environmental_protection_tax"]))
        parm.append(int(row["parm"]))
    return personal_info,income,tax,vat,environmental_protection_tax,parm
            
