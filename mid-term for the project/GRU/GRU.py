import pandas as pd
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import GRU, Dense, Embedding
from keras.utils import pad_sequences
from keras.optimizers import Adam
import numpy as np
import re

df = pd.read_csv('fake_transactional_data_24.csv')

def replace_account_names(name):
    if re.fullmatch(r'\d+', name):
        return 'transaction'
    else:
        return name

#restructure
df['to_randomly_generated_account'] = df['to_randomly_generated_account'].apply(lambda x: replace_account_names(x))

# 找到monopoly_money_amount大于10的行的索引
indices_to_drop = df[df['to_randomly_generated_account'] == 'transaction'].index

# 删除这些行
df = df.drop(indices_to_drop)

# 对商家类型进行编码
merchant_encoder = LabelEncoder()
df['merchant_encoded'] = merchant_encoder.fit_transform(df['to_randomly_generated_account'])

# 标准化交易金额
scaler = MinMaxScaler(feature_range=(0, 1))
df['amount_scaled'] = scaler.fit_transform(df[['monopoly_money_amount']])

# 将数据分成特征和标签
X = df['amount_scaled'].values
y = df['merchant_encoded'].values

# 由于是时间序列问题，我们需要构建一个可以使用过去的交易来预测未来的模型
# 这里假设我们使用过去10次交易来预测下一次商家类型，需要构建这样的序列数据
X_sequences = []
y_sequences = []
for i in range(10, len(X)):
    X_sequences.append(X[i-10:i])
    y_sequences.append(y[i])

X_sequences = np.array(X_sequences)
y_sequences = np.array(y_sequences)

# 序列填充
X_padded = pad_sequences(X_sequences)

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X_padded, y_sequences, test_size=0.2, random_state=42)

optimizer = Adam(learning_rate = 0.01)

# 创建模型
model = Sequential()
model.add(Embedding(input_dim=len(merchant_encoder.classes_), output_dim=6, input_length=X_train.shape[1]))
model.add(GRU(units=128))
model.add(Dense(len(merchant_encoder.classes_), activation='softmax'))

# 编译模型
model.compile(loss='sparse_categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])

# 训练模型
model.fit(X_train, y_train, batch_size=32, epochs=10, validation_data=(X_test, y_test))