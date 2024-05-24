import pandas as pd
import requests
import json

# 读取CSV文件到DataFrame
# train_data = pd.read_csv("train.csv", index_col=0)
train_data = pd.read_csv("train.csv")
print(len(train_data))

# 初始化职位描述摘要列
train_data['job_description_summary'] = None

# 循环遍历DataFrame中的每一行
example_prompt = "你现在是一位求职者。给定职位标题以及职位描述，请根据职位标题和其描述文本总结该职位负责的工作任务。" \
                 "要求是只需要回答职位负责的是什么，不要补充其他内容，尽量从A和B中选出词语进行描述，字数不超过40，回答模版为:该职位负责...。" \
                 "比如当职位标题='信用卡销售'，职位描述='1.负责华夏银行信用卡的营销与办理 2.工作方式自由 3.任务轻松，每天三个，月入过万'，" \
                 "输出:该职位负责信用卡的营销与办理。现在"

for i in range(min(10, len(train_data))):
    # 构建请求的payload
    payload = json.dumps({
        "model": "Nanbeige-16B-Chat-plus",  # 指定使用的模型
        "max_tokens": 4096,  # 最大令牌数限制
        "temperature": 0.7,
        "top_p": 1,
        "output_accumulate": True,
        "messages": [
            {
                "role": "user",  # 角色为用户
                "content": example_prompt + "职位标题" + train_data['job_title'][i]
                           + "，职位描述=" + train_data['job_description'][i] + "，输出：\n"

            }
        ]
    })

    url = "https://stardustlm.zhipin.com/api/gpt/open/chat/openai/send/msg"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IiIsInV1aWQiOiJuYmdfY3NsX3BhcnRuZXJfcGxheWVyOS02NTkzNDhlZS1lZDcyLTQxZGEtYWYwZi05N2E2MGE1MGExMGUifQ.9hTvhNxwncrLvVPG-utFFdUmZDNXA3YmvkWl-RGDJm8'
    }

    # 发送POST请求，获取职位描述的摘要
    response = requests.post(url, headers=headers, data=payload)  # 注意：url和headers需要定义
    content = response.json()['modelServerData']['choices'][0]['message']['content']
    print(str(i) + ": " + content)

    # 检查响应内容是否以“抱歉”开头
    if content.startswith("抱歉"):
        # 如果是，则不更新摘要列
        train_data.loc[i, 'job_description_summary'] = None
    else:
        # 如果不是，则更新摘要列为响应内容的第一个词
        train_data.loc[i, 'job_description_summary'] = content.split()[0]

# 将更新后的DataFrame保存到新的CSV文件
train_data.to_csv("new_train.csv")
