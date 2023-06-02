from flask import Flask, render_template, url_for, request, redirect, jsonify, request
from datetime import datetime, timedelta
import binascii, codecs
import mysql.connector
from question_to_answer import question_text_to_answer
from flask_socketio import SocketIO, emit
from dotenv import load_dotenv
import os
import openai
from query_keyword import query_keyword
from key_to_text import key_to_text
import socketio as sioo
# from exp6 import make_answer

load_dotenv()
openai.api_key = os.environ.get('openai_key')


app = Flask(__name__)
socketio = SocketIO(app)
clients=[]
# sio = sioo.Client()
# sio.connect('http://localhost:5232')

@app.route(f'/donga/test/', methods=['GET'])
def index_brod():
    return render_template('sihwang_with_so.html')
    # return render_template('test.html', article=article, id_0='asdf', state='asdf', state_m='asdf')


def handle_question(question0):
    key_word = query_keyword(question0)
    # Emit keyword
    socketio.emit('my_response', {'data': key_word})

    text0, result_list = key_to_text(key_word)
    # Emit articles
    socketio.emit('my_response', {'data': result_list})

    # Generate and emit answer
    answer = generate_answer(text0, question0)
    socketio.emit('my_response', {'data': answer})

def generate_answer(text0, question0):
    prompt = f"""
                {text0}
                ====================\\
                위 내용들을 바탕으로 대답해줘.
                {question0}
                """
    completion = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
    )
    return completion['choices'][0]['message']['content'].replace('위 기사에서는', '')

@app.route(f'/donga/askhere', methods=['POST'])
def shit():
    question0 = request.form['question0']
    handle_question(question0)
    return 'ok'


if __name__ == "__main__":
    # serve(app, host = '0.0.0.0', port = '3389', threads=1)
    # with open('C:/stamp/port.txt', 'r') as f:
    #     port = f.read().split(',')[0]  # 노트북 5232, 데스크탑 5231
    #     # port = port[0]
    # # print(port)
    # # host = '0.0.0.0'
    # host = 'localhost'
    # # if port == '5232':
    # # host = '172.30.1.58'
    # # host = '0.0.0.0'
    #
    # # elif port == '5231':
    # # port = '5240'
    # # host = '0.0.0.0'
    # port = 5232
    # # 172.30.1.53
    # # 0.0.0.0
    # app.run(host=host, port=port, debug=True)
    host = 'localhost'
    port = 5232  # iteger 이어야함
    socketio.run(app, host=host, port=port, debug=True)