import pandas as pd

# Load the CSV file
data = pd.read_csv("D:/TB2/DSMP/fake_transactional_data_24.csv")

# Look at the first few rows of the data
print(data.head())

# Perform a basic statistical analysis of the amount column
monopoly_money_stats = data['monopoly_money_amount'].describe()
print(monopoly_money_stats)

import matplotlib.pyplot as plt
import seaborn as sns

# Set the chart style
sns.set(style="whitegrid")

# Draw a histogram
plt.figure(figsize=(12, 6))
sns.histplot(data['monopoly_money_amount'], bins=30, kde=True)
plt.title('Distribution of Monopoly Money Amount')
plt.xlabel('Monopoly Money Amount')
plt.ylabel('Frequency')
plt.show()

# Count the number of trades for different accounts
to_account_value_counts = data['to_randomly_generated_account'].value_counts()

# Draw a bar chart
plt.figure(figsize=(12, 8))
to_account_value_counts.plot(kind='bar')
plt.title('Frequency of Transactions to Randomly Generated Accounts')
plt.xlabel('Account')
plt.xticks(rotation=45, ha="right")
plt.ylabel('Frequency')
plt.tight_layout()
plt.show()
