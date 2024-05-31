from gensim.models import Word2Vec
import pandas as pd
import ast
from tqdm import tqdm


def get_most_similar_words(fac_key_words, fac_targets):
    # key_words = [[1,2,3,4,5],[1,2,3,4,5]]
    # targets = [[6,7,8,9,10]]
    # num = 0
    result = []
    for target in tqdm(fac_targets):
        # if num == 10:
        #     break
        fac_key_words.append(target)
        model = Word2Vec(fac_key_words, min_count=1, workers=4)
        similar_words = []
        for word in target:
            similar_words.append(model.wv.most_similar(word)[0][0])
        result.append(similar_words)
        fac_key_words.pop(-1)
        # num = num + 1
    return result


def get_top_five_keys(frequency_dict):
    # 转换为包含 (value, key) 元组的列表
    sorted_items = sorted(frequency_dict.items(), key=lambda x: x[1], reverse=True)
    # 提取前五个元素的键
    top_five_keys = [item[0] for item in sorted_items[:5]]

    return top_five_keys


def get_solution():
    position_file = "./data/position_keywords.csv"
    test_file = "./data/test_keywords.csv"
    result_file = "./data/result.csv"

    position_data = pd.read_csv(position_file)
    simplify_data = position_data.loc[:, ['job_keywords',
                                          'translate_keywords',
                                          'position_name']]

    en_ch_reflect = {}
    en_job_reflect = {}
    key_words = []
    for row in simplify_data.to_dict('records'):
        keywords_ch = row['job_keywords'].split(',')
        keywords_en = ast.literal_eval(row['translate_keywords'])
        position_name = row['position_name']

        key_words.append(keywords_en)

        for i in range(len(keywords_en)):
            en_ch_reflect[keywords_en[i]] = keywords_ch[i]
            if keywords_en[i] in en_job_reflect:
                en_job_reflect[keywords_en[i]].append(position_name)
            else:
                en_job_reflect[keywords_en[i]] = [position_name]

    test_data = pd.read_csv(test_file)
    targets = []
    for row in test_data.to_dict('records'):
        targets.append(ast.literal_eval(row['translate_keywords']))

    word_res = get_most_similar_words(key_words, targets)
    print(word_res)

    result_list = []
    for words in word_res:
        frequency_dict = {}

        for word in words:
            traces = en_job_reflect[word]
            for trace in traces:
                if trace not in frequency_dict:
                    frequency_dict[trace] = 1
                else:
                    frequency_dict[trace] += 1

        result_list.append(get_top_five_keys(frequency_dict))

    print(result_list)
    result = pd.Series(result_list)
    result.to_csv(result_file, header=['id', 'job'], index_label='id')


if __name__ == "__main__":
    get_solution()
