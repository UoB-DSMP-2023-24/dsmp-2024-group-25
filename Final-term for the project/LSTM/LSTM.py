import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
from keras.models import Sequential
from sklearn.model_selection import train_test_split
from keras.utils import to_categorical
from keras.layers import LSTM, Dense
import classification

data = pd.read_csv('/Users/liubohan/Documents/GitHub/dsmp-2024-group-25/Final-term for the project/LSTM/Purchase.csv')

data['Date'] = pd.to_datetime(data['Date'], dayfirst=True)
data['Day'] = (data['Date'] - data['Date'].min()).dt.days
data['Minutes'] = data['Timestamp'].str.split(':').apply(lambda x: int(x[0]) * 60 + int(x[1]))

data = classification.classify_third_party(data)
    
# 将第三方账户名转换为0-9的标签
le = LabelEncoder()
data['Third Party Name'] = le.fit_transform(data['Third Party Name'])



def create_sequences(df, sequence_length=24):
    X = []
    y = []
    
    # 假设 "MinuteOfDay" 已转换为一天中的分钟数
    # 你需要将它转换回小时数，因为我们基于每小时进行预测
    df['HourOfDay'] = df['Minutes'] // 60
    
    for i in range(len(df) - sequence_length):
        # 提取24小时长度的特征序列
        seq = df[['HourOfDay']].iloc[i:i + sequence_length].values
        X.append(seq)
        
        # 假设目标（"Consumption"）位于序列之后的一个小时
        target = df['Third Party Name'].iloc[i + sequence_length]
        y.append(target)
        
    return np.array(X), np.array(y)

X, y = create_sequences(data)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


model = Sequential()
model.add(LSTM(30, return_sequences=False, input_shape=(12, 1)))
model.add(Dense(1))  

model.compile(optimizer='adam', loss='mean_squared_error')
model.fit(X_train, y_train, epochs=10, batch_size=32, validation_split=0.2)

# 评估模型
loss, accuracy = model.evaluate(X_test, y_test)
print(f'Test Loss: {loss}, Test Accuracy: {accuracy}')