import pandas as pd
from datetime import datetime, time

# Load the dataset
income_file_path = 'D:/TB/DSMP/mid/income_transactions.csv'
expense_file_path = 'D:/TB/DSMP/mid/expense_transactions.csv'

income_transactions_df = pd.read_csv(income_file_path)
expense_transactions_df = pd.read_csv(expense_file_path)

# Check and convert the values in the Timestamp column
def convert_time(x):
    if isinstance(x, str) and x.strip() != '':
        try:
            return datetime.strptime(x.strip(), '%H:%M').time()
        except ValueError:
            return None
    else:
        return None
    
# Applying the convertion  function
income_transactions_df['Timestamp'] = income_transactions_df['Timestamp'].apply(convert_time)
expense_transactions_df['Timestamp'] = expense_transactions_df['Timestamp'].apply(convert_time)

# Define time  theresholds
morning_threshold = time(7, 0)
evening_threshold = time(22, 0)

# Flag suspicious time for both datasets
income_transactions_df['Suspicious_Time'] = ((income_transactions_df['Timestamp'] < morning_threshold) |
                                             (income_transactions_df['Timestamp'] > evening_threshold))
expense_transactions_df['Suspicious_Time'] = ((expense_transactions_df['Timestamp'] < morning_threshold) |
                                              (expense_transactions_df['Timestamp'] > evening_threshold))

# Calculate the average inccome  and expense
average_income = income_transactions_df.groupby('Account No')['Amount'].mean()
average_expense = expense_transactions_df.groupby('Account No')['Amount'].mean()

# Flag high-value transfers
income_transactions_df['High_Value_Transaction'] = income_transactions_df.apply(
    lambda row: row['Amount'] > (average_income.get(row['Account No'], 0) * 1.5), axis=1)

expense_transactions_df['High_Value_Transaction'] = expense_transactions_df.apply(
    lambda row: row['Amount'] > (row['Balance'] * 0.5), axis=1)

# Calculate the average number of transfers per account
average_income_transactions_count = income_transactions_df['Account No'].value_counts().mean()
average_expense_transactions_count = expense_transactions_df['Account No'].value_counts().mean()

# Flag high-frequency transfers
income_transactions_df['Frequent_Transactions'] = income_transactions_df['Account No'].map(
    income_transactions_df['Account No'].value_counts()) > (2 * average_income_transactions_count)

expense_transactions_df['Frequent_Transactions'] = expense_transactions_df['Account No'].map(
    expense_transactions_df['Account No'].value_counts()) > (2 * average_expense_transactions_count)

# Filter out all possible fraudulent transfer records
suspicious_income_transactions_df = income_transactions_df[(income_transactions_df['Suspicious_Time'] |
                                                            income_transactions_df['High_Value_Transaction'] |
                                                            income_transactions_df['Frequent_Transactions'])]

suspicious_expense_transactions_df = expense_transactions_df[(expense_transactions_df['Suspicious_Time'] |
                                                              expense_transactions_df['High_Value_Transaction'] |
                                                              expense_transactions_df['Frequent_Transactions'])]

# Save the data
formatted_suspicious_income_transactions_df = suspicious_income_transactions_df.copy()
formatted_suspicious_income_transactions_df['Timestamp'] = formatted_suspicious_income_transactions_df[
    'Timestamp'].apply(lambda x: x.strftime('%H:%M') if x is not None else 'N/A')
suspicious_income_transactions_file_path = 'D:/TB/DSMP/mid/suspicious_income_transactions.csv'
formatted_suspicious_income_transactions_df.to_csv(suspicious_income_transactions_file_path, index=False)

formatted_suspicious_expense_transactions_df = suspicious_expense_transactions_df.copy()
formatted_suspicious_expense_transactions_df['Timestamp'] = formatted_suspicious_expense_transactions_df[
    'Timestamp'].apply(lambda x: x.strftime('%H:%M') if x is not None else 'N/A')
suspicious_expense_transactions_file_path = 'D:/TB/DSMP/mid/suspicious_expense_transactions.csv'
formatted_suspicious_expense_transactions_df.to_csv(suspicious_expense_transactions_file_path, index=False)

# Statistics on detected abnormal accounts
income_transactions_df['Anomaly_Combination'] = income_transactions_df[
    ['Suspicious_Time', 'High_Value_Transaction', 'Frequent_Transactions']].apply(
    lambda row: ', '.join([anomaly for anomaly, flag in
                           zip(['Suspicious_Time', 'High_Value_Transaction', 'Frequent_Transactions'], row)
                           if flag]) or "No Anomaly", axis=1)

expense_transactions_df['Anomaly_Combination'] = expense_transactions_df[
    ['Suspicious_Time', 'High_Value_Transaction', 'Frequent_Transactions']].apply(
    lambda row: ', '.join([anomaly for anomaly, flag in
                           zip(['Suspicious_Time', 'High_Value_Transaction', 'Frequent_Transactions'], row)
                           if flag]) or "No Anomaly", axis=1)

# Save statistics
income_anomaly_statistics_path = 'D:/TB/DSMP/mid/income_anomaly_statistics.csv'
expense_anomaly_statistics_path = 'D:/TB/DSMP/mid/expense_anomaly_statistics.csv'

income_anomaly_combination_counts = income_transactions_df['Anomaly_Combination'].value_counts()
expense_anomaly_combination_counts = expense_transactions_df['Anomaly_Combination'].value_counts()

income_anomaly_combination_counts.to_csv(income_anomaly_statistics_path)
expense_anomaly_combination_counts.to_csv(expense_anomaly_statistics_path)

















