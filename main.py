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
    {"role" : "system", "content" : "You are a helpful assistant to write a python program."}
]

test = [{
    "name": "애플 아이패드 미니6세대 셀룰러 256GB (색상선택)",
    "price": 1225500
  },
  {
    "name": "Apple 아이폰 14 128GB 미개통 미개봉 새상품",
    "price": 1119000
  }
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
    return send_from_directory('gpt_call', 'chat.html')

@app.route('/process_output', methods=['POST'])
def process_output():
    data = request.get_json()
    output = data['output']

    result = {'message' : 'output 작업이 완료되었습니다.'}

    crawling(output)

    product_list = []

    with open('./webCrawling/output.json', 'r') as f:
        product_list = json.load(f)

    '''product_list = []

    for item in jsondata:
        product = {
            "name" : item["name"],
            "price": item["price"],
            "img_url": item["img_url"],
            "goto_url": item["goto_url"],
            "detail": item["detail"]
        }
        product_list.append(product)'''

    #print(jsondata[0])

    for product in product_list: #html에서 product_list만 먼저 받아오기. 리스트가 먼저 출력되야 하기 때문. 
        role = "system"
        content = f'Product Name : {product["name"]}\nPrice: {product["price"]}'
        price_messages.append({"role":role , "content":content})
    price_messages.append({"role":"user", "content": "price 값을 int로 형변환 한 뒤, 1,000,000 이상인 product들을 찾아서 name과 price를 list 형태를 저장하는 python 프로그램을 작성하고, 저장된 list 결과값을 json 형태로 출력해줘."})
    

    price_output = chatGPT(price_messages)
    print(price_output)

    '''price_messages2 = [{"role":"user", "content": "price 값이 1,000,000 이상인 product들을 찾아서 name과 price를 list 형태를 저장하는 python 프로그램을 작성하고, 저장된 list 결과값만 반환해줘. list 결과값을 출력해줘."}]
    price_messages2.append({"role":"assistant", "content":price_output})
    price_messages2.append({"role": "user", "content":"only 저장된 리스트의 속성값만 출력해줘."})
    price_output2 = chatGPT(price_messages2)
    print(price_output2)'''
    
    return jsonify({'product_list' : product_list, 'price_output': price_output})

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
    cmd = f'node ./webCrawling/crawling.js {output}'
    subprocess.run(cmd, shell=True)
    #return send_from_directory('webCrawling', 'app.js')

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, port=5000)
