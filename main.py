from eval import eval_job_classify
from get_job_description_summary import get_job_description_summary
from get_job_keywords import get_job_keywords
from get_secondary_keywords import get_secondary_keywords
from get_result import get_result
from get_test_keywords import get_test_keywords


def main():
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # 跑一次要很久，不要轻易运行!!!!!!!!!!
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # 获取工作的简化描述
    get_job_description_summary()
    # 获取职位和一二级职位的关键词
    get_job_keywords()
    get_secondary_keywords()
    # 获取测试数据中的关键词
    get_test_keywords()
    # 生成结果
    get_result()
    # 运行比较程序
    eval_job_classify()


if __name__ == "__main__":
    main()
