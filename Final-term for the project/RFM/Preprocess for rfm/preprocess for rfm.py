import pandas as pd
import classification

orders = pd.read_csv('/Users/liubohan/Documents/GitHub/dsmp-2024-group-25/Final-term for the project/RFM/Preprocess for rfm/Purchase.csv',sep=',')
orders = orders.drop('Third Party Account No', axis=1)
orders['Amount'] = orders['Amount'].abs()
orders['Account No'] = orders['Account No'].astype(int).astype(str)
orders = classification.classify_third_party(orders)

bc = orders['Third Party Name'] == 'Food & Drink'
bank = orders[bc]

bank.to_csv('rfm-fd.csv', sep=',')