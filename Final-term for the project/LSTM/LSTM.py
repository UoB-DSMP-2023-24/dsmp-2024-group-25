import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler, LabelEncoder
from keras.models import Sequential
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from keras.utils import to_categorical
from keras.layers import LSTM, Dense, Dropout
from keras.callbacks import EarlyStopping

data = pd.read_csv('/Users/liubohan/Documents/GitHub/dsmp-2024-group-25/Final-term for the project/LSTM/Purchase.csv')

data['Weekday'] = data['Datetime'].dt.dayofweek  # 星期一是0，星期天是6
data['Hour'] = data['Datetime'].dt.hour

le = LabelEncoder()
data['Third Party Encoded'] = le.fit_transform(data['Third Party Name'])

category_onehot = to_categorical(data['Third Party Encoded'])

num_categories = len(le.classes_)
num_weekdays = 7
num_hours = 24

account_ids = data['Account No'].unique()

account_matrices = {account_id: np.zeros((num_weekdays, num_hours, num_categories)) for account_id in account_ids}

for _, row in data.iterrows():
    acct_matrix = account_matrices[row['Account No']]
    day = row['Weekday']
    hour = row['Hour']
    acct_matrix[day, hour, :] = category_onehot[_]

num_samples = data.shape[0] * data.shape[1]  # 账户数 * 时间段数
num_features = data.shape[2]  # 类别数
X = data.reshape((num_samples, num_features))
y = data['Third Party Encoded'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = Sequential()
model.add(LSTM(50, input_shape=(X_train.shape[1], X_train.shape[2])))
model.add(Dropout(0.2))
model.add(Dense(y_train.shape[1], activation='softmax'))  # y_train.shape[1]是类别数量

# 编译模型
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# 训练模型
early_stopping = EarlyStopping(monitor='val_loss', patience=10, mode='min')
history = model.fit(X_train, y_train, epochs=100, batch_size=32, validation_split=0.2, callbacks=[early_stopping])

# 评估模型
loss, accuracy = model.evaluate(X_test, y_test)
print(f'Test Loss: {loss}, Test Accuracy: {accuracy}')