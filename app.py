from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

# 将API密钥存储在环境变量中以确保安全性
API_KEY = "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"
BASE_URL = "https://integrate.api.nvidia.com/v1"


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        word = request.form.get('word')
        if not word:
            error = "请输入一个词语。"
            return render_template('index.html', error=error)

        # 构建AI提示词，插入用户输入的词语
        prompt = f"你是新汉语老师、你是年轻人，你批判现实、思考深刻。风格：罗永浩、鲁迅。擅长一针见血、表达隐喻、批判、讽刺、幽默。你会用一个特殊视角来解释一个词汇，精炼表达，委婉解释，精炼表达。当用户输入词语后，你会输出以上风格的新的解释。词语：{word}"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }

        data = {
            "model": "meta/llama-3.1-405b-instruct",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2,
            "top_p": 0.7,
            "max_tokens": 1024,
            "stream": False  # 设置为False以简化处理
        }

        try:
            response = requests.post(f"{BASE_URL}/chat/completions", headers=headers, json=data)
            response.raise_for_status()
            result = response.json()
            # 假设返回结构类似OpenAI的API
            ai_response = ""
            if 'choices' in result:
                for choice in result['choices']:
                    if 'message' in choice and 'content' in choice['message']:
                        ai_response += choice['message']['content']
            else:
                ai_response = "AI未返回有效的响应。"

        except requests.exceptions.RequestException as e:
            ai_response = f"请求AI API时发生错误：{e}"

        return render_template('result.html', word=word, definition=ai_response)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
