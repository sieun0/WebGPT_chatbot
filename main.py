from flask import Flask, send_from_directory
from flask import request, jsonify
from flask_cors import CORS
import os
import openai

app = Flask(__name__)
CORS(app)

#API_KEY= os.getenv("FLASK_API_KEY")


'''def chatGPT():
    # set api key
    openai.api_key = API_KEY 

    # Call the chat GPT API
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
         {"role": "user", "content": f"한국의 대통령은 누구입니까?"},
        ],
        temperature=0,
        max_tokens=2048
    )
    return completion

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, port=5000)'''
@app.route("/")
def chat():
    return send_from_directory('gpt_call', 'chat.html')

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, port=5000)
