import pandas as pd
import numpy as np

# Set random seeds
np.random.seed(42)

# Load dataset
sample_data_path = 'D:/TB2/DSMP/sample_new.xlsx'  
sample_data = pd.read_excel(sample_data_path)

# Randomly generated total amount for source account
source_accounts = sample_data['from_totally_fake_account'].unique()  
source_account_totals = {account: np.random.rand() * 10000 for account in source_accounts} 

# Randomly generated total amount for target account
target_accounts = sample_data['to_randomly_generated_account'].unique()  
target_account_totals = {account: np.random.rand() * 10000 for account in target_accounts}  

# Add the total amount to  the dataset
sample_data['source_account_total'] = sample_data['from_totally_fake_account'].map(source_account_totals)
sample_data['target_account_total'] = sample_data['to_randomly_generated_account'].map(target_account_totals)

# Save the balance
new_data_path = 'D:/TB2/DSMP/balance.xlsx'
sample_data.to_excel(new_data_path, index=False)

print(f'Updated dataset has been saved to {new_data_path}')
