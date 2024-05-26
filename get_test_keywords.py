import pandas as pd

from methods import get_keywords, translate


def get_test_keywords():
    test_file = "data/test.csv"
    result_file = "data/test_keywords.csv"
    test_data = pd.read_csv(test_file)

    test_data['job_keywords'] = None
    test_data['translate_keywords'] = None
    for i in range(len(test_data)):
        test_data['job_keywords'][i] = get_keywords(test_data['job_title'][i],
                                                    test_data['job_description'][i])
        print(str(i) + ": " + test_data['job_keywords'][i])
        keywords = test_data['job_keywords'][i].split(",")
        translated_keywords = []
        for keyword in keywords:
            translated_keywords.append(translate(keyword))
        test_data['translate_keywords'][i] = str(translated_keywords)
        print(test_data['position_name'][i] + ": " + test_data['translate_keywords'][i])
    test_data.to_csv(result_file)


if __name__ == "__main__":
    get_test_keywords()
