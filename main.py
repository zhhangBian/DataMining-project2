from eval import eval_job_classify
from get_job_description_summary import get_job_description_summary
from get_job_keywords import get_job_keywords
from methods import *


def main():
    get_job_description_summary()
    get_job_keywords()

    eval_job_classify()


if __name__ == "__main__":
    main()
