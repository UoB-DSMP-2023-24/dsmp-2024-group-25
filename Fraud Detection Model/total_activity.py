import pandas as pd
from pandas import ExcelWriter

# load the dataset
data_path = 'D:/TB2/aaa/total_balance.csv'
data = pd.read_csv(data_path)

# check the date format
data_type = data['not_happened_yet_date'].dtype
data_type

# convert date format
data['not_happened_yet_date'] = pd.to_datetime(data['not_happened_yet_date'], format='%d/%m/%Y', errors='coerce')

# Calculate the transaction frequency and average transaction amount for each source account
source_account_activity = data.groupby('from_totally_fake_account').agg(
    transactions_count=pd.NamedAgg(column='monopoly_money_amount', aggfunc='count'),
    average_transaction_amount=pd.NamedAgg(column='monopoly_money_amount', aggfunc='mean'),
    total_transaction_amount=pd.NamedAgg(column='monopoly_money_amount', aggfunc='sum')
).reset_index()

# target account
target_account_activity = data.groupby('to_randomly_generated_account').agg(
    transactions_count=pd.NamedAgg(column='monopoly_money_amount', aggfunc='count'),
    average_transaction_amount=pd.NamedAgg(column='monopoly_money_amount', aggfunc='mean'),
    total_transaction_amount=pd.NamedAgg(column='monopoly_money_amount', aggfunc='sum')
).reset_index()

# Add to the balance.xlsx
data = data.merge(source_account_activity, on='from_totally_fake_account', how='left')
data = data.merge(target_account_activity, on='to_randomly_generated_account', how='left')

data.to_csv(data_path, index=False)