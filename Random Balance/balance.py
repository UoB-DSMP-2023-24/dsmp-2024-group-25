import pandas as pd
import numpy as np

def append_balances_to_df_from_file(file_path, seed=42, min_percentage=10, max_percentage=50):

    # Load the dataset
    df = pd.read_csv(file_path)
    
    # Set the seed for reproducibility
    np.random.seed(seed)
    
    # Calculate the sum of transactions for each account
    transaction_totals = df.groupby('from_totally_fake_account')['monopoly_money_amount'].sum()
    
    # Generate a random percentage for each account within the specified range
    random_percentages = np.random.uniform(min_percentage, max_percentage, size=len(transaction_totals)) / 100
    
    # Calculate new balances by applying the random percentage to the transaction totals
    new_balances = transaction_totals * (1 + random_percentages)
    
    # Ensure the account numbers in the original DataFrame match the data type of the index in new_balances
    if new_balances.index.dtype != df['from_totally_fake_account'].dtype:
        df['from_totally_fake_account'] = df['from_totally_fake_account'].astype(new_balances.index.dtype)
    
    # Map the new balances back to the original DataFrame
    df['balance'] = df['from_totally_fake_account'].map(new_balances)
    
    return df

file_path = 'D:/TB2/DSMP/fake_transactional_data_24.csv'
df_updated = append_balances_to_df_from_file(file_path)

# Display the first few rows to verify the 'balance' column
print(df_updated.head())

