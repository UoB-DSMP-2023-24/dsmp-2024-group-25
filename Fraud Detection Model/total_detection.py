import pandas as pd
import numpy as np

# Load the balance data
data_path = 'D:/TB/aaa/first/updated_total_balance.csv'
data = pd.read_csv(data_path)

# Define abnormal account detection function
def detect_anomalies(df):
    # Define high-frequency transactions threshold as twice the mean
    high_freq_threshold = df['Transaction Frequency'].mean() * 2
    high_freq_accounts = df[df['Transaction Frequency'] > high_freq_threshold]
    
    # Define large transactions as exceeding 80% of the total account amount
    large_trans_accounts = df[df['Average Transaction Amount'] > df['source_account_total'] * 0.8]
    
    # Define low-frequency high-value transactions accounts
    low_freq_large_trans_accounts = df[(df['Transaction Frequency'] <= df['Transaction Frequency'].median()) & (df['Average Transaction Amount'] > df['source_account_total'] * 0.8)]
    
    
    anomalies = pd.concat([
        high_freq_accounts.assign(Anomaly_Type='High Frequency'),
        large_trans_accounts.assign(Anomaly_Type='Large Transaction'),
        low_freq_large_trans_accounts.assign(Anomaly_Type='Low Frequency Large Transaction')
    ], ignore_index=True)
    
    return anomalies

# Detect anomaly account
anomalies = detect_anomalies(data)

# Save the output
anomalies.to_csv('D:/TB/aaa/first/anomalies_detected.csv', index=False)