from flask import Flask, render_template, url_for, request, redirect, jsonify
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
load_dotenv()
openai.api_key = os.environ.get('openai_key')
import time

app = Flask(__name__)
socketio = SocketIO(app)



@app.route(f'/donga/test/', methods=['GET'])
def index_brod():


    return render_template('test2.html')
    # return render_template('test.html', article=article, id_0='asdf', state='asdf', state_m='asdf')

@app.route(f'/donga/shit/', methods=['GET'])
def shit():
    return("herhere")
    

    # return render_template('test2.html')
    # return render_template('test.html', article=article, id_0='asdf', state='asdf', state_m='asdf')

@socketio.on('my_event')
def call(data):
    dic = {}
    print(data)
    query = f"#질문 : {data['data']} <br><br>#키워드:"
    dic['data']= query
    emit('my_response0', dic)
    key_word = query_keyword(data['data'])

    
    #키워드
    dic['data']=f"{key_word}<br><br>#추천기사:"
    emit('my_response', dic)

    #기사검색
    text0, result_list = key_to_text(key_word)
    article_list = ''
    for url0, tit0 in result_list:
        article_list += f'<a href="{url0}">{tit0}</a><br>'
    dic['data']=article_list+"<br>#답:"
    emit('my_response2', dic)

    #답
    prompt = f"""
        {text0}
        위 내용들을 바탕으로 대답해줘.
        {data['data']}
        """
    print(prompt)
    completion = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

    )
    print("herererererererer")
    
    answer =f"{completion['choices'][0]['message']['content']} <br>================================="
    print(answer)
    dic['data'] =  answer
    emit('my_response3', dic)

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