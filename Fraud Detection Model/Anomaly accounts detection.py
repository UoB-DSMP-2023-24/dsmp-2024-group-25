import pandas as pd

# Define threshold for abnormal behaviour
# More than 10 transactions per day
HIGH_FREQUENCY_THRESHOLD = 10

# Transaction amount exceeding 5000 within one day
LARGE_TRANSACTION_AMOUNT = 5000

# Less than or equal to 2 transactions per day
LOW_FREQUENCY_THRESHOLD = 2

# Load the activity ddataset
source_account_activity = pd.read_excel('D:/TB2/DSMP/source_account_activity.xlsx')
target_account_activity = pd.read_excel('D:/TB2/DSMP/target_account_activity.xlsx')

# Detect anomaly activities
def detect_anomalies(df, account_type):
    high_freq_accounts = df[df['transactions_count'] > HIGH_FREQUENCY_THRESHOLD].assign(Anomaly_Type='High Frequency')
    large_trans_accounts = df[df['average_transaction_amount'] > LARGE_TRANSACTION_AMOUNT].assign(Anomaly_Type='Large Transaction')
    low_freq_large_trans_accounts = df[(df['transactions_count'] <= LOW_FREQUENCY_THRESHOLD) & (df['average_transaction_amount'] > LARGE_TRANSACTION_AMOUNT)].assign(Anomaly_Type='Low Frequency Large Transaction')
    
    # Merge results
    anomalies = pd.concat([
        high_freq_accounts,
        large_trans_accounts,
        low_freq_large_trans_accounts
    ], ignore_index=True)
    
    # Add account type
    anomalies['Account_Type'] = account_type
    return anomalies

# Filter accounts
filtered_source_account_activity = source_account_activity[source_account_activity['from_totally_fake_account'].astype(str).str.isnumeric()]
filtered_target_account_activity = target_account_activity[target_account_activity['to_randomly_generated_account'].astype(str).str.isnumeric()]

# Detect seperately
source_anomalies = detect_anomalies(filtered_source_account_activity, 'Source')
target_anomalies = detect_anomalies(filtered_target_account_activity, 'Target')

# Save the output
output_path_source = 'D:/TB2/DSMP/source_anomalies.xlsx'
output_path_target = 'D:/TB2/DSMP/target_anomalies.xlsx'

source_anomalies.to_excel(output_path_source, index=False)
target_anomalies.to_excel(output_path_target, index=False)

# 
print(f'Source anomalies have been saved to {output_path_source}')
print(f'Target anomalies have been saved to {output_path_target}')