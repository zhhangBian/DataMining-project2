import nltk
from tqdm import tqdm
import pandas as pd
import ast
import heapq

position_keywords_file = "./data/position_keywords.csv"
test_keywords_file = "./data/test_keywords.csv"
result_id_file = "./data/result_id_list.csv"
result_file = "data/result.csv"


# 获取相似度最大的职业的索引列表
def find_top_similar_job_list(similarity_list, num=10):
    job_index_list = []

    # 使用最大堆找到相似度列表中最大的 num 个元素及其索引
    top_similarities = heapq.nlargest(num, zip(similarity_list, range(len(similarity_list))))

    # 从找到的元素中获取索引
    for similarity, index in top_similarities:
        job_index_list.append(index)

    return job_index_list


# 找到相似度最大的职业
def get_most_similar_position_id_list(position_keywords, test_keywords):
    most_similar_position_list = []
    for test_keyword in tqdm(test_keywords):
        similarity_list = []

        for position_keyword in position_keywords:
            # 计算test和每个position的相似度
            similarity = nltk.translate.bleu_score.sentence_bleu(
                [[a_word for phrase in position_keyword for a_word in phrase.split()]],
                [a_word for phrase in test_keyword for a_word in phrase.split()])
            similarity_list.append(similarity)

        most_similar_position_list.append(find_top_similar_job_list(similarity_list))
    return most_similar_position_list


def get_result():
    position_keywords_data = pd.read_csv(position_keywords_file)
    test_keywords_data = pd.read_csv(test_keywords_file)

    position_keywords_list = []
    test_keyword_list = []

    # 将职位对应的关键词组成一个列表
    for position_row in position_keywords_data.to_dict('records'):
        position_keywords_list.append(ast.literal_eval(position_row['translate_keywords']))

    # 将测试职位对应的关键词组成一个列表
    for test_row in test_keywords_data.to_dict('records'):
        test_keyword_list.append(ast.literal_eval(test_row['translate_keywords']))

    # 通过相似度计算最匹配的id列表
    result_id_list = get_most_similar_position_id_list(position_keywords_list,
                                                       test_keyword_list)
    pd.Series(result_id_list).to_csv(result_id_file)

    # 将id列表转换为职位名列表
    result_data = []
    for job_id_list in result_id_list:
        test_prediction = []
        for job_id in job_id_list:
            test_prediction.append(position_keywords_data[job_id]['position_name'])
        result_data.append(test_prediction)

    pd.Series(result_data).to_csv(result_file)


if __name__ == "__main__":
    get_result()
