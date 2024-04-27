import pandas as pd
import numpy as np

# Set random seeds
np.random.seed(42)

# Load dataset
sample_data_path = 'D:/TB/aaa/fake_transactional_data_24.csv'  
sample_data = pd.read_csv(sample_data_path)

# Randomly generated total amount 
source_accounts = sample_data['from_totally_fake_account'].unique()  
source_account_totals = {account: np.random.rand() * 10000 for account in source_accounts}  

# Add the total amount to  the dataset
sample_data['source_account_total'] = sample_data['from_totally_fake_account'].map(source_account_totals)

# Save
new_data_path = 'D:/TB/aaa/first/new_total_balance.csv'
sample_data.to_csv(new_data_path, index=False)


