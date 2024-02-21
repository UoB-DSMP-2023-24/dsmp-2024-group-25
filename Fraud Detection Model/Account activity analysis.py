import pandas as pd
from pandas import ExcelWriter

# load the dataset
data_path = 'D:/TB2/DSMP/sample_new.xlsx'
data = pd.read_excel(data_path)

# check the date format
data_type = data['not_happened_yet_date'].dtype
data_type

# convert date format
data['not_happened_yet_date'] = pd.to_datetime(data['not_happened_yet_date'])

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

# save the output
output_path_source = 'D:/TB2/DSMP/source_account_activity.xlsx'  
output_path_target = 'D:/TB2/DSMP/target_account_activity.xlsx'  

with ExcelWriter(output_path_source) as writer:
    source_account_activity.to_excel(writer, index=False, sheet_name='Source Account Activity')

with ExcelWriter(output_path_target) as writer:
    target_account_activity.to_excel(writer, index=False, sheet_name='Target Account Activity')