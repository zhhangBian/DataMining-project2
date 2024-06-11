import json


def get_job_json():
    # 读取文件内容
    job_path = "data/job_class.txt"
    result_path = "data/job_json.json"

    with open(job_path, 'r', encoding='utf-8') as file:
        data = file.read()

    # 初始化字典
    categories = {}

    # 逐行处理输入数据
    for line in data.strip().split('\n'):
        level1, level2, level3 = line.split('-')

        if level1 not in categories:
            categories[level1] = {}

        if level2 not in categories[level1]:
            categories[level1][level2] = []

        categories[level1][level2].append(level3)

    # 转换为JSON格式
    json_data = json.dumps(categories, ensure_ascii=False, indent=4)

    # 保存结果到json文件
    with open(result_path, 'w', encoding='utf-8') as json_file:
        json_file.write(json_data)

    # 打印结果
    print(json_data)


if __name__ == "__main__":
    get_job_json()
