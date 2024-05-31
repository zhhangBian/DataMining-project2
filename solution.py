from gensim.models import Word2Vec
import pandas as pd
import ast


def get_most_similar_words(fac_key_words, fac_targets):
    # key_words = [[1,2,3,4,5],[1,2,3,4,5]]
    # targets = [[6,7,8,9,10]]
    # num = 0
    result = []
    for target in fac_targets:
        # if num == 10:
            # break
        fac_key_words.append(target)
        model = Word2Vec(fac_key_words, min_count=1, workers=4)
        similar_words = []
        for word in target:
            similar_words.append(model.wv.most_similar(word)[0][0])
        result.append(similar_words)
        fac_key_words.pop(-1)
        # num += 1
    return result


def find_top_five_keys(dictionary):  
    # 转换为包含 (value, key) 元组的列表  
    sorted_items = sorted(dictionary.items(), key=lambda x: x[1], reverse=True)  
      
    # 提取前五个元素的键  
    top_five_keys = [item[0] for item in sorted_items[:5]]  # 这里应该是 item[0] 而不是 item[1]  
      
    return top_five_keys


df = pd.read_csv('./data/position_keywords.csv')
tmp = df.loc[:, ['job_keywords', 'translate_keywords', 'position_name']]

en_ch_reflect = {}
en_job_reflect = {}
key_words = []
for row in tmp.to_dict('records'):
    ch = row['job_keywords'].split(',')
    en = ast.literal_eval(row['translate_keywords'])
    job = row['position_name']
    key_words.append(en)
    for i in range(len(en)):
        en_ch_reflect[en[i]] = ch[i]
        if en[i] in en_job_reflect:
            en_job_reflect[en[i]].append(job)
        else:
            en_job_reflect[en[i]] = [job]
key_words[0]


ts_df = pd.read_csv('./data/test_keywords.csv')
targets = []
for row in ts_df.to_dict('records'):
    targets.append(ast.literal_eval(row['translate_keywords']))
targets[0]

word_res = get_most_similar_words(key_words, targets)


res = []
for words in word_res:
    freq = {}

    for word in words:
        traces = en_job_reflect[word]
        for trace in traces:
            if trace not in freq:
                freq[trace] = 1
            else:
                freq[trace] += 1

    res.append(find_top_five_keys(freq))


print(res)
