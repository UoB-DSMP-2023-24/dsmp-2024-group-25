from torch.utils.data import Dataset
import os
import pandas as pd
import torch



class MyDataset(Dataset):
    def __init__(self, file_path):
        self.data = []
        self.target = []
        self.filepath = file_path
        self.max = 0
        self.process()
        
        
    def __len__(self):
        return len(self.data)
        
    
    def __getitem__(self, index):
        data = []
        zero_tensor = torch.zeros(1, 2)
        for i in range(len(self.data[index])):
            item = torch.tensor(self.data[index][i]).reshape(1, -1)
            data.append(item)

        for i in range(self.max - len(self.data[index])):
            data.append(zero_tensor)
        data = torch.cat(data, dim=0)
        target = torch.tensor(self.target[index])
        return data, target
        


    def process(self):
        data = pd.read_csv(self.filepath)
        data['Timestamp'] = pd.to_datetime(data['Timestamp'])
        data['Balance'] = (data['Balance'] - data['Balance'].mean()) / data['Balance'].std()
        data['Amount'] = (data['Amount'] - data['Amount'].mean()) / data['Amount'].std()
        grouped = data.groupby(pd.Grouper(key='Timestamp', freq='1H'))
        account_lists = []

        #每次迭代 account_groups，都会处理一个特定的账户在该时间段内的数据
        #并将这些数据作为一个列表加入到 account_lists 中
        #这意味着 account_lists 的每一个元素是特定时间段内某个账户的所有交易记录
        for _, group in grouped:
            if not group.empty:
                account_groups = group.groupby('Account No')
                for _, account_group in account_groups:
                    account_lists.append(account_group.values.tolist())

        # print(account_lists[0])
        
        
        #存储每个账户在特定时间内的tag概率
        for i in range(len(account_lists)):
            new_list = [0] * 10
            for j in range(len(account_lists[i])):
                new_list[account_lists[i][j][-1]] += 1
                del account_lists[i][j][0]
                del account_lists[i][j][0]
                del account_lists[i][j][-1]
            listsum = sum(new_list)
            if self.max < listsum:
                self.max = listsum
            self.target.append([element / listsum for element in new_list])
            
        self.data = account_lists

    def getmax(self):
        return self.max

    

    