from question_to_answer import question_text_to_answer
from flask_socketio import SocketIO, emit
from dotenv import load_dotenv
import os
import openai
from query_keyword import query_keyword
from key_to_text import key_to_text
import socketio as sioo
load_dotenv()
openai.api_key = os.environ.get('openai_key')
sio = sioo.Client()
sio.connect('http://localhost:5232')

def make_answer(question0):
    print(question0)
    key_word = query_keyword(question0)

    dic = {}
    # 키워드
    dic['data'] = key_word
    sio.emit('my_event', dic)

    # 기사검색
    text0, result_list = key_to_text(key_word)
    article_list = ''
    for url0, tit0 in result_list:
        article_list += f'<a href="{url0}">{tit0}</a><br>'
    dic['data'] = article_list
    sio.emit('my_event', dic)

    # 답
    prompt = f"""
            {text0}
            ====================
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
    answer = completion['choices'][0]['message']['content'].replace('위 기사에서는', '')
    dic['data'] = answer
    sio.emit('my_event', dic)
    return True