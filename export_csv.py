import csv
def write_data_to_csv(data,file_name):
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        for item in data:
            writer.writerow(item)
