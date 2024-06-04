import nltk
from tqdm import tqdm
import pandas as pd
import ast

position_keywords_file = "./data/position_keywords.csv"
test_keywords_file = "./data/test_keywords.csv"
result_file = "data/result.csv"


def find_top_similar_job_list(similarity_list, num=10):
    job_index_list = []
    reflect = {}
    for i in range(len(similarity_list)):
        reflect[similarity_list[i]] = i

    similarity_list.sort(reverse=True)
    for i in range(num):
        job_index_list.append(reflect[similarity_list[i]])
    return job_index_list


def get_most_similar_words(fac_key_words, fac_targets):
    result = []
    for target in tqdm(fac_targets):
        similarity_list = []
        for my_word in fac_key_words:
            similarity_list.append(nltk.translate.bleu_score.sentence_bleu(
                [[a_word for phrase in my_word for a_word in phrase.split()]],
                [a_word for phrase in target for a_word in phrase.split()])
            )
        result.append(find_top_similar_job_list(similarity_list))
    return result


def get_result():
    position_keywords_data = pd.read_csv(position_keywords_file)

    key_words_list = []

    select_row = position_keywords_data.loc[:, ['job_keywords',
                                                'translate_keywords',
                                                'position_name']]
    for row in select_row.to_dict('records'):
        # 转换类型为列表
        job_keywords_list_en = ast.literal_eval(row['translate_keywords'])
        key_words_list.append(job_keywords_list_en)

    test_keywords_data = pd.read_csv(test_keywords_file)

    targets = []
    position_name_list = position_keywords_data.loc[:, 'position_name'].tolist()
    for row in test_keywords_data.to_dict('records'):
        targets.append(ast.literal_eval(row['translate_keywords']))

    most_similarity_list = get_most_similar_words(key_words_list, targets)

    result_data = []
    for job_id_list in most_similarity_list:
        test_prediction = []
        for job_id in job_id_list:
            test_prediction.append(position_name_list[job_id])
        result_data.append(test_prediction)

    pd.Series(result_data).to_csv(result_file)


if __name__ == "__main__":
    get_result()
