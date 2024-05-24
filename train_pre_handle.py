import pandas as pd

from methods import get_job_description_summary

# 读取CSV文件到DataFrame
# train_data = pd.read_csv("train.csv", index_col=0)
train_data = pd.read_csv("new_train.csv")
print(len(train_data))

# 初始化职位描述摘要列
# train_data['job_description_summary'] = None

for i in range(10495, len(train_data)):
    train_data.loc[i, 'job_description_summary'] = (
        get_job_description_summary(train_data['job_title'][i], train_data['job_description'][i][0:3800]))

    print(str(i) + ": " + train_data.loc[i, 'job_description_summary'])
    train_data.to_csv("new_train.csv")

# 将更新后的DataFrame保存到新的CSV文件
train_data.to_csv("new_train.csv")
