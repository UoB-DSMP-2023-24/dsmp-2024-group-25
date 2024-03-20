import pandas as pd

# Load data
file_path = 'D:/TB/DSMP/mid/simulated_transaction_2024.csv'
transactions_df = pd.read_csv(file_path)

# Filter the transactions
pure_number_transactions = transactions_df[pd.to_numeric(transactions_df['Third Party Account No'], errors='coerce').notnull()]

# Save the data
filtered_file_path = 'D:/TB/DSMP/mid/filtered_transaction_2024.csv'
pure_number_transactions.to_csv(filtered_file_path, index = False)
