import pandas as pd

from methods import get_job_keywords

with open('JobClass.txt', 'r', encoding='utf-8') as file:
    classes = file.read().splitlines()  # 读取所有行并将其分割成列表

train_data = 'train.csv'  # 替换为你的CSV文件路径
train_pd = pd.read_csv(train_data)

# 进行分类
descriptions_by_class = train_pd.groupby('position_name')['job_description'].apply(list).to_dict()

# 创建一个字典，其中键是类别，值是描述列表，确保每个类别都有对应的描述列表，即使某些类别在CSV文件中没有描述
class_description_dict = {cls: descriptions_by_class.get(cls, []) for cls in classes}

# 将结果保存为csv格式
df_class_descriptions = pd.DataFrame(list(class_description_dict.items()),
                                     columns=['position_name', 'job_description'])
output_position_csv_path = 'position_descriptions.csv'
df_class_descriptions.to_csv(output_position_csv_path, index=False, encoding='utf-8-sig')

keywords_list = []
for position_name, job_description in class_description_dict.items():
    job_keywords = get_job_keywords(position_name, str(job_description))
    keywords_list.append((position_name, job_keywords))
    print(position_name + ": " + job_keywords)

df_keywords = pd.DataFrame(keywords_list, columns=['position_name', 'job_keywords'])
output_keywords_csv_path = 'position_keywords.csv'
df_keywords.to_csv(output_keywords_csv_path, index=False, encoding='utf-8-sig')