import pandas as pd

from methods import separate_job_class, get_merge_keywords, translate


def get_secondary_keywords():
    separate_job_class()

    keywords_file = "data/position_keywords.csv"
    result_file = "data/first_second_keywords.csv"

    keywords_data = pd.read_csv(keywords_file)
    keywords_data['first_second'] = keywords_data['position_name'].apply(
        lambda x: '-'.join(x.split('-')[:2]))

    grouped = keywords_data.groupby('first_second')['job_keywords'].apply(
        lambda x: ','.join(x)).reset_index()
    grouped.to_csv(result_file, index=False)

    grouped['merge_keywords'] = None
    grouped['translate_keywords'] = None
    for i in range(len(grouped)):
        grouped['merge_keywords'][i] = get_merge_keywords(str(grouped['first_second'][i]),
                                                          str(grouped['job_keywords'][i]))
        print(grouped['first_second'][i] + ": " + str(grouped['merge_keywords'][i]))

        keywords = grouped['merge_keywords'][i].split(",")
        translated_keywords = []
        for keyword in keywords:
            translated_keywords.append(translate(keyword))
        grouped['translate_keywords'][i] = str(translated_keywords)
        print(grouped['translate_keywords'][i])

    grouped.to_csv(result_file, index=False)


if __name__ == "__main__":
    get_secondary_keywords()
