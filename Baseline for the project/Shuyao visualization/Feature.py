import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import matplotlib.pyplot as plt

## Load the dataset
df = pd.read_csv('C:/Users/Lenovo/Downloads/fake_transactional_data_24.csv')

# Use 10% of the data as a sample
df = df.sample(frac=0.1, random_state=42)  


def classify_business_simplified(business_name):
    # First, check if it's a pure numerical transfer record
    if business_name.isdigit():
        return 'Transfer'

    # Convert to lowercase for comparison
    lower_name = business_name.lower()
    
    # Automatically classify based on keywords
    if any(keyword in lower_name for keyword in ['coffee', 'cafe']):
        return 'Coffee Shop'
    elif 'bar' in lower_name or 'pub' in lower_name:
        return 'Bar'
    elif any(keyword in lower_name for keyword in ['lunch', 'restaurant','takeaway']):
        return 'Restaurant'
    elif any(keyword in lower_name for keyword in ['shop', 'store', 'boutique', 'market']):
        return 'Shop'
    elif 'gym' in lower_name:
        return 'Gym'
    elif 'supermarket' in lower_name:
        return 'Supermarket'
    elif 'cinema' in lower_name or 'streaming' in lower_name:
        return 'Entertainment'

    #  Manual mapping for special cases or businesses that cannot be automatically classified by keywords
    special_mapping = {
    'TURKEY_FARM': 'Other',  
    'FLORIST': 'Shop',
    'TO_BEAN_OR_NOT_TO_BEAN': 'Coffee Shop',
    'WE_HAVE_BEAN_WEIGHTING': 'Coffee Shop',
    'KIDS_ACTIVITY_CENTRE': 'Entertainment',
    'LOCAL_WATERING_HOLE': 'Bar',
    'BUTCHERS': 'Other',  
    'GREENGROCER': 'Other', 
    'STEAK_HOUSE': 'Restaurant',  
    'SEAFOOD_RESAURANT': 'Restaurant', 
    'ROASTERIE': 'Coffee Shop', 
    'WINE_CELLAR': 'Shop',  
    'BUTCHER': 'Other',  
    }

    return special_mapping.get(business_name, 'Other')  # Default to 'Other' if not in mapping

# Convert dates and extract time features
df['not_happened_yet_date'] = pd.to_datetime(df['not_happened_yet_date'], format='%d/%m/%Y')
df['weekday'] = df['not_happened_yet_date'].dt.weekday  
df['is_weekend'] = df['weekday'].apply(lambda x: 1 if x >= 5 else 0)  
df['month'] = df['not_happened_yet_date'].dt.month  
df['is_mid_month'] = df['not_happened_yet_date'].dt.day.apply(lambda x: 1 if x == 16 else 0)  # mid-month
df['is_month_end'] = df['not_happened_yet_date'].dt.day.apply(lambda x: 1 if x in [29, 30, 31] else 0)  # end of month

# Assign transaction type for each row in DataFrame
df['transaction_type'] = df['to_randomly_generated_account'].apply(classify_business_simplified)

# Convert transaction types to numerical features with one-hot encoding, keeping time features
df_encoded = pd.get_dummies(df, columns=['transaction_type'])

# Define features and target variable
X = df_encoded.drop(['to_randomly_generated_account', 'not_happened_yet_date', 'monopoly_money_amount'], axis=1)
y = df_encoded['monopoly_money_amount']

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model using RandomForestRegressor
model = RandomForestRegressor(n_estimators=10, max_depth=10, random_state=42, n_jobs=-1)
model.fit(X_train, y_train)

# Evaluate feature importance
feature_importances = pd.Series(model.feature_importances_, index=X.columns).sort_values(ascending=False)
print(feature_importances.index)

# Visualize feature importance
plt.figure(figsize=(10, 6))
feature_importances.plot(kind='bar')
plt.title('Feature Importance')
plt.ylabel('Importance Score')
plt.xlabel('Feature')
plt.show()

print("Training finished.\n")