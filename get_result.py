import nltk
from tqdm import tqdm


def find_top_five_indices(nums):
    res = []
    reflect = {}
    for i in range(len(nums)):
        reflect[nums[i]] = i
    nums.sort(reverse=True)
    for i in range(5):
        res.append(reflect[nums[i]])
    return res


def get_most_similar_words(fac_key_words, fac_targets):
    # key_words = [[1,2,3,4,5],[1,2,3,4,5]]
    # targets = [[6,7,8,9,10]]
    # print(fac_key_words)
    # print(fac_targets)
    num = 0
    result = []
    for target in tqdm(fac_targets):
        # if num == 10:
        #     break
        num += 1

        scores = []
        for my_word in fac_key_words:
            # print([[a_word for phrase in my_word for a_word in phrase.split()]])
            # print([[a_word for phrase in target for a_word in phrase.split()]])
            scores.append(nltk.translate.bleu_score.sentence_bleu(
                [[a_word for phrase in my_word for a_word in phrase.split()]],
                [a_word for phrase in target for a_word in phrase.split()])
            )
            # print(scores)
            # return None
        result.append(find_top_five_indices(scores))
    return result


def get_result():
    import pandas as pd
    df = pd.read_csv('./data/position_keywords.csv')

    tmp = df.loc[:, ['job_keywords', 'translate_keywords', 'position_name']]

    import ast
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

    ts_df = pd.read_csv('./data/test_keywords.csv')
    tmp = pd.read_csv('./data/position_keywords.csv')
    tmp = tmp.loc[:, 'position_name']
    jobs = tmp.tolist()
    targets = []
    for row in ts_df.to_dict('records'):
        targets.append(ast.literal_eval(row['translate_keywords']))

    word_res = get_most_similar_words(key_words, targets)
    final_res = []
    for f_res in word_res:
        temp = []
        for f in f_res:
            temp.append(jobs[f])
        final_res.append(temp)

    pd.Series(final_res).to_csv('data/result.csv')


if __name__ == "__main__":
    get_result()
