import pandas as pd

data = pd.read_csv('Business.csv')

data_income = data[data['Amount'] > 0]

data_purchase = data[data['Amount'] < 0]

csv_income = '/Users/liubohan/Documents/GitHub/dsmp-2024-group-25/Final-term for the project/Income.csv'
data_income.to_csv(csv_income, index=False)

csv_purchase = '/Users/liubohan/Documents/GitHub/dsmp-2024-group-25/Final-term for the project/Purchase.csv'
data_purchase.to_csv(csv_purchase, index=False)