import pandas as pd

from methods import get_keywords

train_data_file = "data/new_train.csv"
job_keywords_file = "data/position_keywords.csv"
job_descriptions_file = "data/position_descriptions.csv"
job_class_file = 'data/job_class.txt'


def get_job_keywords():
    with open(job_class_file, 'r', encoding='utf-8') as file:
        classes = file.read().splitlines()

    train_pd = pd.read_csv(train_data_file)
    descriptions_by_class = train_pd.groupby('position_name')['job_description_summary'].apply(list).to_dict()

    # 创建字典，其中键是类别，值是描述列表
    class_description_dict = {cls: descriptions_by_class.get(cls, []) for cls in classes}

    result = []
    for position_name, job_descriptions in class_description_dict.items():
        job_keywords = get_keywords(position_name, str(job_descriptions))
        result.append((position_name, job_descriptions, job_keywords))
        print(position_name + ": " + job_keywords)

    df_keywords = pd.DataFrame(result, columns=['position_name', 'job_descriptions', 'job_keywords'])
    df_keywords.to_csv(job_keywords_file, index=False, encoding='utf-8-sig')


if __name__ == "__main__":
    get_job_keywords()
