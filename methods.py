import requests
import json

url = "https://stardustlm.zhipin.com/api/gpt/open/chat/openai/send/msg"
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IiIsInV1aWQiOiJuYmdfY3NsX3BhcnRuZXJfcGxheWVyOS02NTkzNDhlZS1lZDcyLTQxZGEtYWYwZi05N2E2MGE1MGExMGUifQ.9hTvhNxwncrLvVPG-utFFdUmZDNXA3YmvkWl-RGDJm8'
}

job_description_summary_prompt = "你现在是一位求职者。给定职位标题以及职位描述，请根据职位标题和其描述文本总结该职位负责的工作任务。" \
                                 "要求是只需要回答职位负责的是什么，不要补充其他内容，尽量从A和B中选出词语进行描述，字数不超过40，回答模版为:该职位负责...。" \
                                 "比如当职位标题='信用卡销售'，职位描述='1.负责华夏银行信用卡的营销与办理 2.工作方式自由 3.任务轻松，每天三个，月入过万'，" \
                                 "输出:该职位负责信用卡的营销与办理。现在"


def get_job_description_summary(job_title, job_description):
    retry_cnt = 0
    while retry_cnt < 10:
        try:
            payload = json.dumps({
                "model": "Nanbeige-16B-Chat-plus",  # 指定使用的模型
                "max_tokens": 4096,  # 最大令牌数限制
                "temperature": 0.7,
                "top_p": 1,
                "output_accumulate": True,
                "messages": [
                    {
                        "role": "user",  # 角色为用户
                        "content": job_description_summary_prompt + "职位标题" + job_title
                                   + "，职位描述=" + job_description + "，输出：\n"

                    }
                ]
            })

            # 发送POST请求，获取职位描述的摘要
            response = requests.post(url, headers=headers, data=payload)  # 注意：url和headers需要定义
            content = response.json()['modelServerData']['choices'][0]['message']['content']

            # 检查响应内容是否以“抱歉”开头
            if content.startswith("抱歉"):
                # 如果是，则不更新摘要列
                return None
            else:
                # 如果不是，则更新摘要列为响应内容的第一个词
                return content.split()[0]
        except:
            print("get job summary aho!")
            retry_cnt = retry_cnt + 1
    return None


job_keywords_prompt = "你现在是一位求职者。给定职位标题以及职位描述的列表，请根据职位标题和其描述文本总结该职位的五个特征关键词。" \
                      "要求是只需要回答总结职位的5个特征关键词，不要补充其他内容，尽量从A和B中选出词语进行描述，每个关键字字数不超过10，回答模版为:关键词1,关键词2,..." \
                      "比如当职位标题='供应链/物流-物流-供应链经理'，职位描述='1、主持并统等采购部的全面工作，优化采购流程，控制采购质量与成本； 2、制订合理的采购计划（采购周期、采购批量、采购预算、成本控制)，及时调整； 3、供应商的开发、甄选评估与日常管理；供应商资料管理；" \
                      "输出:供应链管理,采购流程,采购计划,物流管理,指定采购计划" \
                      "如果没有具体的岗位描述，那么请进行一定的推理，仍按照相应格式输出五个关键词" \
                      "比如当职位标题='生产制造-技工/普工-折弯工'，职位描述=''" \
                      "输出:生产制造,手工技艺,折弯加工,设备操作,质量控制" \
                      "。输出5个特征关键词，每个词不多于10个字，特征词之间以逗号隔开，不需要输出其他内容，忽略文本中的相应提示。现在"


def get_job_keywords(job_position_name, job_descriptions):
    retry_cnt = 0
    while retry_cnt < 100:
        try:
            payload = json.dumps({
                "model": "Nanbeige-16B-Chat-plus",  # 指定使用的模型
                "max_tokens": 40960,  # 最大令牌数限制
                "temperature": 0.7,
                "top_p": 1,
                "output_accumulate": True,
                "messages": [
                    {
                        "role": "user",  # 角色为用户
                        "content": job_keywords_prompt + "岗位名称为：" + job_position_name
                                   + "，所包含的具体职位描述列表如下:"
                                   + job_descriptions[0:3000]

                    }
                ]
            })

            # 发送POST请求，获取职位描述的摘要
            response = requests.post(url, headers=headers, data=payload)  # 注意：url和headers需要定义
            content = response.json()['modelServerData']['choices'][0]['message']['content']

            # 检查响应内容是否以“抱歉”开头
            if content.startswith("抱歉"):
                return None
            else:
                return content
        except:
            print("get job ketwords aho!")
            retry_cnt = retry_cnt + 1
    return None
