import pandas as pd
df = pd.read_csv('./database/100_employeers.csv')

def remove_last_digit(x):
    try:
        return int(x) // 10  # Sử dụng phép chia lấy nguyên để loại bỏ chữ số cuối
    except:
        return x  # Trả lại giá trị ban đầu nếu không phải số
    
df['aggregate_income'] = df['aggregate_income'].apply(lambda x: remove_last_digit(x))

df.to_csv('updated_data.csv', index=False)
# aggregate_income,tax,vat,environmental_protection_tax