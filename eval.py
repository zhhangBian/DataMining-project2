import csv
import pandas as pd
import argparse


# 按照岗位描述对岗位进行分类

def recall_at_k(label_list, prediction_list, k):
    correct_recall = 0
    for ind in range(len(label_list)):
        # 确保k不超过列表长度
        tmpk = min(k, len(prediction_list[ind]))
        # 获取前k个预测结果
        top_k_predictions = prediction_list[ind][:tmpk]
        # 计算预测结果中正确答案的数量
        if label_list[ind] in top_k_predictions:
            correct_recall += 1

    recall = correct_recall / len(label_list)
    return recall


def eval_job_classify():
    parser = argparse.ArgumentParser(description="Process a list of texts with BERT")
    parser.add_argument("--pre_path", type=str)
    parser.add_argument("--test_path", type=str)
    args = parser.parse_args()

    testdata = pd.read_csv(args.test_path)
    label_list = list(testdata['position_name'])
    predict_data = pd.read_csv(args.pre_path)
    predict_list = list(predict_data['Prediction'])
    predict_list = [eval(x) for x in predict_list]
    print(recall_at_k(label_list, predict_list, 1))
    print(recall_at_k(label_list, predict_list, 3))
    print(recall_at_k(label_list, predict_list, 5))
    print(recall_at_k(label_list, predict_list, 10))


# python eval.py --pre_path data/result.csv --test_path data/test.csv
if __name__ == "__main__":
    eval_job_classify()
