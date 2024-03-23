import classification
import pandas as pd

data = pd.read_csv('/Users/liubohan/Documents/GitHub/dsmp-2024-group-25/Final-term for the project/LSTM/Purchase.csv')


new_data = classification.classify_third_party(data)

print(new_data['Third Party Name'].unique())