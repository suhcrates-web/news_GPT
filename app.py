from flask import Flask, render_template, url_for, request, redirect, jsonify
from datetime import datetime, timedelta
import binascii, codecs
import mysql.connector
from question_to_answer import question_text_to_answer



app = Flask(__name__)


@app.route(f'/donga/dangbun/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route(f'/donga/AskD/', methods=['GET'])
def index_brod():
    now = datetime.today()
    try:

        article = "질문을 입력하세요"
    
        return render_template('sihwang.html', article=article, id_0='asdf', state='asdf', state_m='asdf')
        # return render_template('test.html', article=article, id_0='asdf', state='asdf', state_m='asdf')

    except:
        article = "<br><br>새로고침 하세요<br><br><br>"
        # date0 = now.strftime("%Y년 %m월 %d일 // %H시 %M분")
        return render_template('sihwang.html', article=article, id_0='asdf', state='asdf', state_m='asdf')
        # return render_template('test.html', article=article, id_0='asdf', state='asdf', state_m='asdf')

@app.route('/donga/ask', methods=['POST'])
def si_post():
    if request.method == 'POST':


        cmd = request.form['cmd']
        question0 = request.form['question0']

        if cmd == 'giveme':

            now = datetime.today()
            answer0 = question_text_to_answer(question0)

        return {"message": answer0, "cmd": 'ok', "time": now.strftime(
            "%Y년 %m월 %d일 // %H시 %M분".encode('unicode-escape').decode()
        ).encode().decode('unicode-escape')}



#잘못들어갈때
@app.route(f'/donga/dangbun/naver/', methods=['GET'])
def mistake1():
    return redirect('http://testbot.ddns.net:5235/donga/dangbun/naver/only')



if __name__ == "__main__":
    # serve(app, host = '0.0.0.0', port = '3389', threads=1)
    with open('C:/stamp/port.txt', 'r') as f:
        port = f.read().split(',')[0]  # 노트북 5232, 데스크탑 5231
        # port = port[0]
    # print(port)
    # host = '0.0.0.0'
    if port == '5232':
        host = '172.30.1.58'
        host = '0.0.0.0'

    elif port == '5231':
        port = '5240'
        host = '0.0.0.0'
    # port = 5233
    # 172.30.1.53
    # 0.0.0.0
    app.run(host=host, port=port, debug=True)
