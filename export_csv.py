import csv
def write_data_to_csv(data,file_name):
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        for item in data:
            writer.writerow(item)

# data=[["long","lan","lien"],["a","b",1000],["c","d",4],["e","f",13131]]
# write_data_to_csv(data,"./message/business_revenue_table.csv")