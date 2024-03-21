import pandas as pd

data = pd.read_csv('simulated_transaction_2024_cleaned.csv')

third_party_account = data[data['Third Party Account No'].notna()]

third_party_business = data[data['Third Party Account No'].isna()]

csv_account = '/Users/liubohan/Documents/GitHub/dsmp-2024-group-25/Final-term for the project/Transactions.csv'
third_party_account.to_csv(csv_account, index=False)

csv_business = '/Users/liubohan/Documents/GitHub/dsmp-2024-group-25/Final-term for the project/Business.csv'
third_party_business.to_csv(csv_business, index=False)
