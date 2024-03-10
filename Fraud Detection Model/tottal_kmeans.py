import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
import numpy as np
import os

# 设置环境变量以避免内存泄露问题
os.environ['OMP_NUM_THREADS'] = '1'

# 加载数据集
data = pd.read_csv('D:/TB2/aaa/total/total_balance.csv')  # 请替换为实际文件路径

# 转换列类型为数值型
columns_to_convert = [
    'monopoly_money_amount', 'source_account_total', 'target_account_total',
    'transactions_count_x', 'average_transaction_amount_x', 'total_transaction_amount_x',
    'transactions_count_y', 'average_transaction_amount_y', 'total_transaction_amount_y'
]

for column in columns_to_convert:
    data[column] = pd.to_numeric(data[column], errors='coerce')

# 选择聚类特征
features = data[columns_to_convert]

# 数据标准化
scaler = StandardScaler()
features_scaled = scaler.fit_transform(features)

# 确定最佳聚类数
silhouette_scores = []
K_range = range(2, 11)  # 测试的聚类数范围
for K in K_range:
    kmeans = KMeans(n_clusters=K, n_init=10, random_state=42)
    cluster_labels = kmeans.fit_predict(features_scaled)
    silhouette_avg = silhouette_score(features_scaled, cluster_labels)
    silhouette_scores.append(silhouette_avg)

# 绘制轮廓系数与聚类数的关系图
plt.figure()
plt.plot(K_range, silhouette_scores, 'bx-')
plt.xlabel('聚类数 (k)')
plt.ylabel('轮廓系数')
plt.title('轮廓系数法确定最佳聚类数')
plt.show()

# 选择轮廓系数最高的聚类数
optimal_K = K_range[silhouette_scores.index(max(silhouette_scores))]
print('最佳聚类数为:', optimal_K)

# 使用最佳聚类数重新聚类
kmeans = KMeans(n_clusters=optimal_K, n_init=10, random_state=42)
data['cluster'] = kmeans.fit_predict(features_scaled)

# 后续步骤：检测异常账户等

# 分析1: 计算每个聚类中的账户数量
cluster_counts = data['cluster'].value_counts()

# 分析2: 计算每个聚类的平均交易特征
cluster_averages = data.groupby('cluster').mean()

# 分析3: 检测不寻常的交易模式或异常账户
# 定义“不寻常”的阈值
unusual_thresholds = {
    'monopoly_money_amount': 1.5,  # 交易金额高于平均值的150%
    'transactions_count_x': 1.5,   # 交易次数高于平均值的150%
}

# 确保更新下面的路径以保存异常账户数据
unusual_accounts = pd.DataFrame()  # 创建一个空DataFrame用于存储异常账户
for cluster in range(optimal_K):
    cluster_data = data[data['cluster'] == cluster]
    unusual_criteria = (cluster_data['monopoly_money_amount'] > data['monopoly_money_amount'].mean() * 1.5) | \
                       (cluster_data['transactions_count_x'] > data['transactions_count_x'].mean() * 1.5)
    unusual_accounts = pd.concat([unusual_accounts, cluster_data[unusual_criteria]])

# 保存异常账户数据
unusual_accounts.to_csv('D:/TB2/aaa/anomaly_accounts.csv', index=False)