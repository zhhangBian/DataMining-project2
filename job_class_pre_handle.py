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
df_class_descriptions.to_csv(output_position_csv_path, index=False)
df_class_descriptions.to_csv(output_position_csv_path, index=False, encoding='utf-8-sig')

example_prompt = "你现在是一位求职者。给定职位标题以及职位描述的列表，请根据职位标题和其描述文本总结该职位的五个特征关键词。" \
                 "要求是只需要回答总结职位的5个特征关键词，不要补充其他内容，尽量从A和B中选出词语进行描述，每个关键字字数不超过10，回答模版为:关键词1,关键词2,..." \
                 "比如当职位标题='供应链/物流-物流-供应链经理'，职位描述='1、主持并统等采购部的全面工作，优化采购流程，控制采购质量与成本； 2、制订合理的采购计划（采购周期、采购批量、采购预算、成本控制)，及时调整； 3、供应商的开发、甄选评估与日常管理；供应商资料管理；" \
                 "输出:供应链管理,采购流程,采购计划,物流管理,指定采购计划" \
                 "如果没有具体的岗位描述，那么请进行一定的推理，仍按照相应格式输出五个关键词" \
                 "比如当职位标题='生产制造-技工/普工-折弯工'，职位描述=''" \
                 "输出:生产制造,手工技艺,折弯加工,设备操作,质量控制" \
                 "，不要输出'关键词1：'这种形式，并且严格控制输出5个关键词，每个字数控制在10以内，现在"

for position_name, job_description in class_description_dict.items():
    print(position_name + ": " + get_job_keywords(position_name, str(job_description)))
