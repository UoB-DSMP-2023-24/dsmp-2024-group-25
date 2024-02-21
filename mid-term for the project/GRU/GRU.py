import pandas as pd
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import GRU, Dense, Embedding
from keras.utils import pad_sequences
from keras.optimizers import Adam
import numpy as np
import re

df = pd.read_csv('fake_transactional_data_24_backup.csv')

df['not_happened_yet_date'] = pd.to_datetime(df['not_happened_yet_date'])
df['year_week'] = df['not_happened_yet_date'].dt.strftime('%Y-%U')

#data restructure
food_and_drinks = ['A_CAFE', 'A_LOCAL_COFFEE_SHOP', 'CAFE', 'CHINESE_RESTAURANT', 'CHINESE_TAKEAWAY', 'COFFEE_SHOP', 'GOURMET_COFFEE_SHOP', 'HIPSTER_COFFEE_SHOP', 'INDIAN_RESTAURANT', 'KEBAB_SHOP', 'LOCAL_RESTAURANT', 'LUNCH_PLACE', 'LUNCH_VAN', 'PRETENTIOUS_COFFEE_SHOP', 'RESTAURANT', 'RESTAURANT_VOUCHER', 'ROASTERIE', 'SANDWICH_SHOP', 'SEAFOOD_RESAURANT', 'STEAK_HOUSE', 'TAKEAWAY', 'TAKEAWAY_CURRY', 'TOTALLY_A_REAL_COFFEE_SHOP']
groceries_and_ds = ['A_SUPERMARKET', 'BUTCHER', 'BUTCHERS', 'DEPARTMENT_STORE', 'EXPRESS_SUPERMARKET', 'GREENGROCER', 'LARGE_SUPERMARKET', 'THE_SUPERMARKET', 'TO_BEAN_OR_NOT_TO_BEAN', 'TURKEY_FARM', 'WE_HAVE_BEAN_WEIGHTING']
clothing_and_jewellery = ['ACCESSORY_SHOP', 'CLOTHES_SHOP', 'FASHION_SHOP', 'FASHIONABLE_SPORTSWARE_SHOP', 'JEWLLERY_SHOP', 'KIDS_CLOTHING_SHOP']
outdoor = ['BAR', 'CINEMA', 'COCKTAIL_BAR', 'G&T_BAR', 'LIQUOR_STORE', 'LOCAL_PUB', 'LOCAL_WATERING_HOLE', 'PUB', 'WHISKEY_BAR', 'WHISKEY_SHOP', 'WINE_BAR', 'WINE_CELLAR']
indoor = ['BOOKSHOP', 'COMIC_BOOK_SHOP', 'DVD_SHOP', 'GAME_SHOP', 'LOCAL_BOOKSHOP', 'NERDY_BOOK_STORE', 'SECOND_HAND_BOOKSHOP', 'STREAMING_SERVICE', 'TOY_SHOP', 'VIDEO_GAME_STORE']
daily_implement = ['CHILDRENDS_SHOP', 'COOKSHOP', 'DIY_STORE', 'ELECTRONICS_SHOP', 'GYM', 'HIPSTER_ELECTRONICS_SHOP', 'HOME_IMPROVEMENT_STORE', 'KIDS_ACTIVITY_CENTRE', 'PET_SHOP', 'PET_TOY_SHOP', 'RUNNING_SHOP', 'SCHOOL_SUPPLY_STORE', 'SPORT_SHOP', 'TEA_SHOP', 'TECH_SHOP', 'TRAINER_SHOP', 'FLORIST']

def replace_account_names(name, a, b, c, d, e, f):
    if re.fullmatch(r'\d+', name):
        return 'transaction'
    
    elif name in a:
        return 'Food & Drink'
    
    elif name in b:
        return 'Groceries & Department Store'
    
    elif name in c:
        return 'Clothing & Jewellery'
    
    elif name in d:
        return 'Outdoor Entertainment'
    
    elif name in e:
        return 'Indoor Entertainment'
    
    elif name in f:
        return 'Daily Purchase'

    else:
        return name

#restructure
df['to_randomly_generated_account'] = df['to_randomly_generated_account'].apply(lambda x: replace_account_names(x, food_and_drinks, groceries_and_ds, clothing_and_jewellery, outdoor, indoor, daily_implement))

# 找到monopoly_money_amount大于10的行的索引
indices_to_drop = df[df['to_randomly_generated_account'] == 'transaction'].index

# 删除这些行
df = df.drop(indices_to_drop)

weekly_sales = df.groupby(['to_randomly_generated_account', 'year_week'])['monopoly_money_amount'].sum().reset_index()

# fd_sales = weekly_sales[weekly_sales['to_randomly_generated_account'] == 'Food & Drink']

# # 数据标准化
# scaler = MinMaxScaler(feature_range=(0, 1))
# fd_sales['scaled_amount'] = scaler.fit_transform(fd_sales[['monopoly_money_amount']])

# time_steps = 2

# X, y = [], []

# for i in range(len(fd_sales) - time_steps):
#     X.append(fd_sales['scaled_amount'].iloc[i:i+time_steps].values)
#     y.append(fd_sales['scaled_amount'].iloc[i+time_steps])

# X, y = np.array(X), np.array(y)

# X = np.reshape(X, (X.shape[0], X.shape[1], 1))

# # 定义GRU模型
# model = Sequential()
# model.add(GRU(units=50, return_sequences=False, input_shape=(time_steps, 1)))
# model.add(Dense(1))

# # 编译模型
# model.compile(optimizer=Adam(learning_rate=0.01), loss='mean_squared_error', metrics=['accuracy'])

# # 划分训练集和测试集
# split_idx = int(len(X) * 0.8)
# X_train, X_test = X[:split_idx], X[split_idx:]
# y_train, y_test = y[:split_idx], y[split_idx:]

# # 训练模型
# history = model.fit(X_train, y_train, epochs=20, batch_size=32, validation_data=(X_test, y_test), verbose=1)


def generate_series_data(weekly_sales, account_type, n_steps):
    scaler = MinMaxScaler(feature_range=(0, 1))
    
    # 获取一个商户类型的销售数据
    sales_data = weekly_sales[weekly_sales['to_randomly_generated_account'] == account_type]
    total_sales = sales_data['monopoly_money_amount'].values.reshape(-1, 1)
    scaled_sales = scaler.fit_transform(total_sales)
    
    # 序列化时间序列数据
    X, y = [], []
    for i in range(len(scaled_sales) - n_steps):
        X.append(scaled_sales[i:i+n_steps])
        y.append(scaled_sales[i+n_steps])
    
    return np.array(X), np.array(y)

def build_and_train_model(X, y):
    # 数据集再分割为训练集和测试集
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 初始化GRU模型
    model = Sequential()
    model.add(GRU(units=50, activation='relu', input_shape=(X_train.shape[1], 1)))
    model.add(Dense(units=1))
    model.compile(optimizer=Adam(learning_rate=0.01), loss='mean_squared_error', metrics=['accuracy'])
    
    # 训练模型
    model.fit(X_train, y_train, epochs=30, batch_size=4, validation_data=(X_test, y_test))
    
    return model

merchant_types = weekly_sales['to_randomly_generated_account'].unique()

n_steps = 4  # 假设过去4个时间步长（周）为基础

for m_type in merchant_types:
    print(f"Processing: {m_type}")
    X, y = generate_series_data(weekly_sales, m_type, n_steps)
    X = X.reshape(X.shape[0], X.shape[1], 1)  # 重塑以符合GRU的输入格式
    m_model = build_and_train_model(X, y)
    # 这里可以加上保存模型的步骤

