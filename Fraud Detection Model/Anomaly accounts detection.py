# Load the required libraries
import pandas as pd
import numpy as np

# Load the balance data
balance_data_path = 'D:/TB2/DSMP/balance.xlsx'
balance_data = pd.read_excel(balance_data_path)

# Display the first few rows of the balance data to understand its structure
balance_data.head()

# Define abnormal account detection function
def detect_anomalies(df):
    # Define high-frequency trading threshold as twice the mean
    high_freq_threshold = df['transactions_count_x'].mean() * 2
    high_freq_accounts = df[df['transactions_count_x'] > high_freq_threshold]
    
    # Define large transactions as exceeding 80% of the total account amount
    large_trans_accounts = df[df['average_transaction_amount_x'] > df['source_account_total'] * 0.8]
    
    # Define low-frequency high-value trading accounts
    low_freq_large_trans_accounts = df[(df['transactions_count_x'] <= df['transactions_count_x'].median()) & (df['average_transaction_amount_x'] > df['source_account_total'] * 0.8)]
    
    # Merge the accounts
    anomalies = pd.concat([high_freq_accounts.assign(Anomaly_Type='High Frequency'),
                           large_trans_accounts.assign(Anomaly_Type='Large Transaction'),
                           low_freq_large_trans_accounts.assign(Anomaly_Type='Low Frequency Large Transaction')], ignore_index=True)
    return anomalies

# Detect anomaly account
anomalies = detect_anomalies(balance_data)

# Save the output
anomalies.to_excel('D:/TB2/DSMP/anomalies_detected.xlsx', index=False)
