import pandas as pd
from datetime import datetime

# Load the dataset
filtered_file_path = 'D:/TB/DSMP/mid/filtered_transaction_2024.csv'
filtered_transactions_df = pd.read_csv(filtered_file_path)

# Remove  missing values
filtered_transactions_df = filtered_transactions_df.dropna(subset=['Account No', 'Amount'])

# Check and convert the values in the Timestamp column
def convert_time(x):
    if isinstance(x, str) and x.strip() != '':
        try:
            return datetime.strptime(x.strip(), '%H:%M').time()
        except ValueError:
            return None
    else:
        return None

filtered_transactions_df['Timestamp'] = filtered_transactions_df['Timestamp'].apply(convert_time)

# Adding Transaction Type column based on Amount
filtered_transactions_df['Transaction Type'] = filtered_transactions_df['Amount'].apply(lambda x: 'Income' if x > 0 else 'Expense')

# Spliting the dataset into income and expensee
income_df = filtered_transactions_df[filtered_transactions_df['Transaction Type'] == 'Income']
expense_df = filtered_transactions_df[filtered_transactions_df['Transaction Type'] == 'Expense']

# Save new dataset
income_df.to_csv('D:/TB/DSMP/mid/income_transactions.csv', index=False)
expense_df.to_csv('D:/TB/DSMP/mid/expense_transactions.csv', index=False)