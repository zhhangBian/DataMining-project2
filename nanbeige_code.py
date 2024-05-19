import requests
import json

url = "https://stardustlm.zhipin.com/api/gpt/open/chat/openai/send/sync"

payload = json.dumps({
  "model": "Nanbeige-16B-Chat",
  "max_tokens": 4096,
  "messages": [
    {
      "role": "user",
      "content": "你好"
    }
  ]
})
headers = {
  'Content-Type': 'application/json',
  'Authorization': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IiIsInV1aWQiOiJuYmdfY3NsX3BhcnRuZXJfcGxheWVyOS02NTkzNDhlZS1lZDcyLTQxZGEtYWYwZi05N2E2MGE1MGExMGUifQ.9hTvhNxwncrLvVPG-utFFdUmZDNXA3YmvkWl-RGDJm8'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.json())
