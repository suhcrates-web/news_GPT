from flask import Flask, render_template, url_for, request, redirect, jsonify
from datetime import datetime, timedelta
import binascii, codecs
import torch


app = Flask(__name__)
@app.route(f'/donga/dangbun/', methods=['GET'])
def index():
    return render_template('index.html')

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
        port = '5234'
        host = '0.0.0.0'
    # port = 5233
    # 172.30.1.53
    # 0.0.0.0
    app.run(host=host, port=port, debug=True)
