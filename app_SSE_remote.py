from flask import Flask, render_template, Response, request, session
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
from flask_cors import CORS
from urllib.parse import unquote
app = Flask(__name__)
CORS(app) # 이렇게 해야 다른 서버에서 보낸것도 다 받게 됨
#CORS(app, resources={r"/set_data": {"origins": "http://localhost:5232"}})  #이렇게 하면 특정 url에서 온거만 허가함
app.secret_key='1234'


# @app.route(f'/donga/test/', methods=['GET'])
# def index_brod():
    # return render_template('test_SSE.html')


@app.route('/set_data', methods=['POST'])
def set_data():
    print('here')
    session['data'] = request.form.get('data')
    print(session['data'])
    return ''

@app.route("/stream")
def stream():
    print('fuck')
    print('fuck')
    data = request.args.get('data')
    # data = session.get('data','')
    data = unquote(data)
    print(data)
    def event_stream():
        #질문
        back1 = f"#질문 : {data} <br><br>#키워드:"
        yield f"data: {back1}\n\n"

        #키워드
        key_word = query_keyword(data)
        back2 = f"{key_word}<br><br>#추천기사:"
        yield f"data: {back2}\n\n"

        #기사검색
        text0, result_list = key_to_text(key_word)
        article_list = ''
        for url0, tit0 in result_list:
            article_list += f'<a href="{url0}">{tit0}</a><br>'
        back3 = article_list+"<br>#답:"
        yield f"data: {back3}\n\n"

        #답
        prompt = f"""{text0}\n\n위 내용들을 바탕으로 대답해줘.\n{data}
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
        yield f"data: {answer}\n\n"
        yield f"data: end\n\n"

    return Response(event_stream(), mimetype="text/event-stream")


if __name__ == "__main__":

    host = 'localhost'
    port = 8001  # iteger 이어야함
    app.run(host=host, port=port, debug=True)
