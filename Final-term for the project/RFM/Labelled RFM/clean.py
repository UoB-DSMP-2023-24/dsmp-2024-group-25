import pandas as pd

orders = pd.read_csv('/Users/liubohan/Documents/GitHub/dsmp-2024-group-25/Final-term for the project/RFM/Labelled RFM/rfm-table-ac.csv',sep=',')

orders.drop(orders.columns[0], axis=1, inplace=True)

orders.to_csv('rfm-table-ac.csv', index=False)

