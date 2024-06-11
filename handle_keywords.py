import ast
import re

import pandas as pd
from tqdm import tqdm


def handle_keywords(file, row):
    # 读取 CSV 文件到 DataFrame
    keywords_data = pd.read_csv(file)

    # 检查 'translate_keywords' 列是否存在
    if row not in keywords_data.columns:
        print("DataFrame 中不存在对应列。")
        return

    # 创建一个新的列表来存储清理过的关键词列表
    cleaned_keywords_list = []

    # 遍历 DataFrame 的行
    for i in tqdm(range(len(keywords_data))):
        try:
            # 获取 'translate_keywords' 列的值并转换为列表
            keywords_list = ast.literal_eval(keywords_data.at[i, row])

            # 清理每个关键词
            cleaned_list = [re.sub(r'[^A-Za-z\s]', '', keyword) for keyword in keywords_list]

            # 将清理过的关键词列表添加到新的列表中
            cleaned_keywords_list.append(cleaned_list)

        except (ValueError, SyntaxError) as e:
            print(f"在索引 {i} 处出现错误：{e}")
            cleaned_keywords_list.append([])  # 如果出错，添加一个空列表

    keywords_data[row] = cleaned_keywords_list
    print(keywords_data[row])
    keywords_data.to_csv(file)


if __name__ == "__main__":
    position_keywords_file = "./data/position_keywords.csv"
    test_keywords_file = "./data/test_keywords.csv"

    handle_keywords(test_keywords_file, "translate_keywords")
    handle_keywords(position_keywords_file, "translate_keywords")