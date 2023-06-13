from flask import Flask, send_from_directory
from flask import request, jsonify
from flask_cors import CORS
import os
import openai
import subprocess
import json

app = Flask(__name__)
CORS(app)

API_KEY= os.getenv("FLASK_API_KEY")

msg_prompt = {
    'recommand' : {
        'system' : "You are a helpful assistant who hepls me recommend the products searched in the chatbot conversation system.",
        'user' : "Write 1 sentence of a simple greeting that starts with '물론이죠! 제가 상품을 추천해드릴게요.'"
    },
    'comparison' : {
        'system' : "You are an assistant who can compare prices in the chatbot conversation system.",
        'user' : "Please write a simple greeting starting with '물론이죠. 말씀하신 상품의 가격을 비교할게요."
    },
    'summarization' : {
        'system' : "You are a helpful assistant to summarize the review.",
        'user' : "Write 1 sentence of a simple greeting that starts with '물론이죠! 이 상품의 리뷰를 요약해드리겠습니다.'"
    }
}

def chatGPT(messages):
    # set api key 
    openai.api_key = API_KEY 

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7,
        max_tokens=2048
    )
    return completion


'''if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, port=5000)'''

@app.route("/")
def chat():
    return send_from_directory('gpt_call', 'chat.html')

@app.route('/process_output', methods=['POST'])
def process_output():
    data = request.get_json()
    output = data['output']

    result = {'message' : ' output 작업이 완료되었습니다.'}

    crawling(output)

    with open('./webCrawling/output.json', 'r') as f:
        jsondata = json.load(f)

    return jsonify(result)

@app.route('/process_input', methods=['POST'])
def process_input():
    data = request.get_json()
    input = data['input']

    result = {'message' : 'input 작업이 완료되었습니다.'}
    chatGPT(messages)

    print(input)

    return jsonify(result)

@app.route('/')
def crawling(output):
    cmd = f'node ./webCrawling/crawling.js {output}'
    subprocess.run(cmd, shell=True)
    #return send_from_directory('webCrawling', 'app.js')

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, port=5000)
