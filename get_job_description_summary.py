import pandas as pd

from methods import get_description_summary


def get_job_description_summary():
    train_file = "data/train.csv"
    new_train_file = "data/new_train.csv"

    train_data = pd.read_csv(train_file)
    print(len(train_data))

    train_data['job_description_summary'] = None

    for i in range(len(train_data)):
        train_data.loc[i, 'job_description_summary'] = (
            get_description_summary(train_data['job_title'][i],
                                    train_data['job_description'][i][0:3500]))

        print(str(i) + ": " + train_data.loc[i, 'job_description_summary'])
        train_data.to_csv(new_train_file)

    train_data.to_csv(new_train_file)


if __name__ == "__main__":
    get_job_description_summary()
