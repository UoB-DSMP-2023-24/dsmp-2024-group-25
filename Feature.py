import pandas as pd
import numpy as np
df = pd.read_csv('C:/Users/Lenovo/Downloads/fake_transactional_data_24.csv')
print(df.info())
# 将日期列转换为日期类型
df['not_happened_yet_date'] = pd.to_datetime(df['not_happened_yet_date'], format='%d/%m/%Y')
df['year'] = df['not_happened_yet_date'].dt.year
df['month'] = df['not_happened_yet_date'].dt.month
df['day'] = df['not_happened_yet_date'].dt.day
df['weekday'] = df['not_happened_yet_date'].dt.weekday  # 周一为0，周日为6

#特征可视化
# import matplotlib.pyplot as plt
# import seaborn as sns

# # 例如，查看不同月份的转账金额分布
# sns.boxplot(x='month', y='monopoly_money_amount', data=df)
# plt.show()

# # 查看一周中各天的转账金额中位数
# sns.barplot(x='weekday', y='monopoly_money_amount', data=df, estimator=np.median)
# plt.show()
