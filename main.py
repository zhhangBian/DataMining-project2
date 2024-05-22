import pandas as pd
import requests
import json

# 读取CSV文件到DataFrame
# train_data = pd.read_csv("train.csv", index_col=0)
train_data = pd.read_csv("train.csv")
# print(train_data['job_title'])

# 初始化职位描述摘要列
train_data['job_description_summary'] = None

# 循环遍历DataFrame中的每一行
for i in range(len(train_data)):
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
                "content": f"职位标题:{train_data['job_title'][i]}\n"
                           f"职位描述:{train_data['job_description'][i]}\n"
                           "请用一句话总结该职位的描述\n"
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
