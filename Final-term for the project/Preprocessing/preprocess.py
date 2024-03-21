import pandas as pd

data = pd.read_csv('simulated_transaction_2024.csv')

data_cleaned = data.dropna(thresh=(len(data.columns) - 1))

cleaned_csv_file_path = '/Users/liubohan/Documents/GitHub/dsmp-2024-group-25/Final-term for the project/simulated_transaction_2024_cleaned.csv'
data_cleaned.to_csv(cleaned_csv_file_path, index=False)