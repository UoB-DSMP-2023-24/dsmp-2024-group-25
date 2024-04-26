import pandas as pd

# Load datasets
income_data = pd.read_csv('D:/TB/DSMP/mid/income_transactions.csv')
expense_data = pd.read_csv('D:/TB/DSMP/mid/expense_transactions.csv')

# Ensure correct data types
income_data['Account No'] = income_data['Account No'].astype(float)
expense_data['Account No'] = expense_data['Account No'].astype(float)
income_data['Amount'] = income_data['Amount'].astype(float)
expense_data['Amount'] = expense_data['Amount'].astype(float)

# Calculate average income per account
average_income = income_data.groupby('Account No')['Amount'].mean().reset_index()
average_income.rename(columns={'Amount': 'Average Income'}, inplace=True)

# Merge datasets based on Account No
merged_data = pd.merge(expense_data, average_income, on='Account No')

# Calculate the percentage of each expense relative to the average income of the account
merged_data['Transaction Ratio'] = merged_data['Amount'].abs() / merged_data['Average Income']

# Add a new column for the response strategy
merged_data['Response Strategy'] = 'No action'

# Apply response strategies based on transaction ratios
for index, transaction in merged_data.iterrows():
    if transaction['Transaction Ratio'] > 0.5:
        merged_data.at[index, 'Response Strategy'] = 'Account will be frozen for security reasons.'
    elif transaction['Transaction Ratio'] > 0.3:
        merged_data.at[index, 'Response Strategy'] = 'A warning message will be sent to the user.'
    elif transaction['Transaction Ratio'] > 0.1:
        merged_data.at[index, 'Response Strategy'] = 'User will be prompted to verify transaction safety before proceeding.'

# Filter transactions where the expense exceeds 30% of the average income
high_ratio_transactions = merged_data[merged_data['Transaction Ratio'] > 0.1]

# Save high-ratio transactions to a new dataset
high_ratio_transactions.to_csv('D:/TB/DSMP/mid/high_ratio_transactions.csv', index=False)



