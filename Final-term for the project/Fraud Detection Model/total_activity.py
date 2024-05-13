import pandas as pd

# Load the new dataset
new_data_path = 'D:/TB/aaa/first/new_total_balance.csv'
data = pd.read_csv(new_data_path)

# Calculate the transaction frequency for each source account
transaction_frequency = data['from_totally_fake_account'].value_counts()

# Calculate the average transaction amount for each source account
average_transaction_amount = data.groupby('from_totally_fake_account')['monopoly_money_amount'].mean()

# update the original dataset
data['Transaction Frequency'] = data['from_totally_fake_account'].map(transaction_frequency)
data['Average Transaction Amount'] = data['from_totally_fake_account'].map(average_transaction_amount)

# Save the updated dataset
updated_data_path = 'D:/TB/aaa/first/updated_total_balance.csv'
data.to_csv(updated_data_path, index=False)

print(f'Updated dataset with transaction frequency and average transaction amount has been saved to {updated_data_path}')


