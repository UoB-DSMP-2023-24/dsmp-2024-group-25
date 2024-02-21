import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from keras.models import Sequential
from keras.layers import Dense
from keras.optimizers import Adam
import re



df = pd.read_csv('fake_transactional_data_24_backup.csv')

df['not_happened_yet_date'] = pd.to_datetime(df['not_happened_yet_date'])
df['year_week'] = df['not_happened_yet_date'].dt.strftime('%Y-%U')

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

# 假设使用'monopoly_money_amount'列来定义消费类别
# 这里的阈值是示例，您需要根据实际数据分布来设置
bins = [0, 100, 200, np.inf]  # 0-100为低，100-200为中，200以上为高
labels = ['low', 'medium', 'high']
df['consumption_category'] = pd.cut(df['monopoly_money_amount'], bins=bins, labels=labels, right=False)

# 将标签转换为数值
label_encoder = LabelEncoder()
df['consumption_category_encoded'] = label_encoder.fit_transform(df['consumption_category'])

X = df.drop(['to_randomly_generated_account', 'consumption_category', 'consumption_category_encoded', 'not_happened_yet_date', 'year_week', 'monopoly_money_amount'], axis=1)
y = df['consumption_category_encoded']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=17)

model = Sequential([
    Dense(64, activation='relu', input_shape=(X_train.shape[1],)),
    Dense(64, activation='relu'),
    Dense(len(labels), activation='softmax')  # 输出层节点数为类别数
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# 数据标准化
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 训练模型
history = model.fit(X_train_scaled, y_train, validation_split=0.2, epochs=30, batch_size=64, verbose=1)

predictions = model.predict(X_test_scaled)
predicted_classes = np.argmax(predictions, axis=1)

predicted_labels = label_encoder.inverse_transform(predicted_classes)

# 如果y_test是数字编码的标签，先解码成原始标签
true_labels = label_encoder.inverse_transform(y_test)

# 查看预测结果与真实结果
for true, pred in zip(true_labels[:10], predicted_labels[:10]):  # 仅展示前10个结果
    print(f'True: {true}, Predicted: {pred}')


