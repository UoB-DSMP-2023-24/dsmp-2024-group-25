import pandas as pd
from datetime import datetime
from datetime import time

# Load dataset
filtered_file_path = 'D:/TB/DSMP/mid/filtered_transaction_2024.csv'
filtered_transactions_df = pd.read_csv(filtered_file_path)


# Check and convert the values in the Timestamp column
def convert_time(x):
    # Check whether it is a non-empty string
    if isinstance(x, str) and x.strip() != '':
        try:
            # convert
            return datetime.strptime(x.strip(), '%H:%M').time()
        except ValueError:
            # If failed, return to None
            return None
    else:
        # For empty cells or non-string values, return to None
        return None

# Apply the conversion function
filtered_transactions_df['Timestamp'] = filtered_transactions_df['Timestamp'].apply(convert_time)

# Define the time of the exception
morning_threshold = time(7, 0)
evening_threshold = time(22, 0)

# Flag a transfer made at an unusual time
filtered_transactions_df['Suspicious_Time'] = (
    (filtered_transactions_df['Timestamp'] < morning_threshold) |
    (filtered_transactions_df['Timestamp'] > evening_threshold)
)

# Calculate the average number of transfers per account and flag accounts that trade frequently
average_transactions_count = filtered_transactions_df['Account No'].value_counts().mean()
frequent_transactions = filtered_transactions_df['Account No'].value_counts()
frequent_transactions_accounts = frequent_transactions[frequent_transactions > 2 * average_transactions_count].index
filtered_transactions_df['Frequent_Transactions'] = filtered_transactions_df['Account No'].isin(frequent_transactions_accounts)

# Flag unusually high value transactions
filtered_transactions_df['High_Value_Transaction'] = filtered_transactions_df['Amount'] > (filtered_transactions_df['Balance'] * 0.5)

# Filter out all possible fraudulent transfer records
suspicious_transactions_df = filtered_transactions_df[(filtered_transactions_df['Suspicious_Time'] | 
                                                       filtered_transactions_df['Frequent_Transactions'] | 
                                                       filtered_transactions_df['High_Value_Transaction'])]

# Outputs samples of suspicious transaction records
print(suspicious_transactions_df.head().to_string(formatters={'Timestamp': lambda x: x.strftime('%H:%M') if x is not None else 'N/A'}))

# Save the data to a new csv file
formatted_suspicious_transactions_df = suspicious_transactions_df.copy()
formatted_suspicious_transactions_df['Timestamp'] = formatted_suspicious_transactions_df['Timestamp'].apply(lambda x: x.strftime('%H:%M') if x is not None else 'N/A')

suspicious_transactions_file_path = 'D:/TB/DSMP/mid/suspicious_transactions.csv'
formatted_suspicious_transactions_df.to_csv(suspicious_transactions_file_path, index=False)

