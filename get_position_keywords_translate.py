import pandas as pd

from methods import translate


def get_position_keywords_translate():
    keywords_file = "data/position_keywords.csv"

    keywords_data = pd.read_csv(keywords_file)

    keywords_data['translate_keywords'] = None
    for i in range(len(keywords_data)):
        keywords = keywords_data['job_keywords'][i].split(",")
        translated_keywords = []
        for keyword in keywords:
            translated_keywords.append(translate(keyword))
        keywords_data['translate_keywords'][i] = str(translated_keywords)
        print(keywords_data['position_name'][i] + ": " + keywords_data['translate_keywords'][i])

    keywords_data.to_csv(keywords_file, index=False)


if __name__ == "__main__":
    get_position_keywords_translate()
