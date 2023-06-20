from flask import Flask, send_from_directory
from flask import request, jsonify
from flask import render_template
from flask_cors import CORS

import os
import openai
import subprocess
import json

app = Flask(__name__)
#CORS(app)

API_KEY= os.getenv("FLASK_API_KEY")

msg_prompt = {
    'Recommendation' : {
        'system' : "You are a helpful assistant to recommend the products searched in the chatbot conversation system.",
        'user' : "Write 1 sentence of a simple greeting that starts with '물론이죠! 제가 상품을 추천해드릴게요.'"
    },
    'Comparison' : {
        'system' : "You are an assistant who can compare prices in the chatbot conversation system.",
        'user' : "Write 1 sentence of a simple greeting that starts with '물론이죠! 말씀하신 상품의 가격을 비교해드릴게요.'"
    },
    'Summarization' : {
        'system' : "You are a helpful assistant to summarize the review.",
        'user' : "Write 1 sentence of a simple greeting that starts with '물론이죠! 이 상품의 리뷰를 요약해드리겠습니다.'"
    },
    'intent' : {
        'system' : "You are a helpful assistant who understands the intent of the user's question.",
        'user' : "Which category does the sentence below belong to: 'Search', Recommendation', 'Comparison', 'Summarization'? Show only categories."
    } 
}

price_messages = [
    {"role" : "system", "content" : "You are a helpful assistant to print out only product_list."}
]

def set_prompt(intent, input, msg_prompt):
    m = dict()
    if('Recommendation' in intent) or ('Search' in intent):
        msg = msg_prompt['Recommendation']
    elif('Comparison' in intent):
        msg = msg_prompt['Comparison']
    elif('Summarization' in intent):
        msg = msg_prompt['Summarization']
    else:
        msg = msg_prompt['intent']
        msg['user'] += f' {input} \n A:'
    for k, v in msg.items():
        m['role'], m['content'] = k, v
    return [m]


def chatGPT(messages):
    # set api key 
    openai.api_key = API_KEY 

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7,
        max_tokens=2048
    )
    return completion['choices'][0]['message']['content']

'''if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, port=5000)'''

@app.route("/")
def chat():
    return send_from_directory('gpt_call', 'chat_copy.html')
  


@app.route('/process_output', methods=['POST'])
def process_output():
    data = request.get_json()
    output = data['output']

    result = {'message' : 'output 작업이 완료되었습니다.'}

    crawling(output)

    product_list = []

    with open('./webCrawling/output.json', 'r') as f:
        product_list = json.load(f)

    #print(product_list)
    
    return jsonify({'product_list' : product_list})

@app.route('/process_input', methods=['POST'])
def process_input():
    data = request.get_json()
    input = data['input']

    result = {'message' : 'input 작업이 완료되었습니다.'}
    user_intent = set_prompt('intent', input, msg_prompt)
    user_intent = chatGPT(user_intent)
    
    #print(input)
    print(user_intent)

    intent_data = set_prompt(user_intent, input, msg_prompt)
    intent_data_msg = chatGPT(intent_data).replace("\n", "").strip()
    
    print(intent_data_msg)

    return jsonify({'intent_data_msg' : intent_data_msg})

@app.route('/')
def crawling(output):
    cmd = f'node ./webCrawling/crawling.js "{output}"'
    #cmd = ['node', './webCrawling/crawling.js', "{output}"]
    subprocess.run(cmd, shell=True)
    #return send_from_directory('webCrawling', 'app.js')

@app.route("/crawl")
def crawldata():
    return send_from_directory('webCrawling', 'output.json')

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, port=5000)
