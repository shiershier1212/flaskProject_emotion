import json
import re
import sqlite3

from flask import Flask, request
from flask_cors import CORS

import myUtils
from jd_spider import spider

app = Flask(__name__)

cors = CORS(app)
from main import predict
from Segment import Seg


def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError


@app.route('/')
def hello_world():
    # ans = predict('物流很快，活动价格买的，很实惠。物品也不错，挺好的购物体验。')
    print('')
    return ''


@app.route('/sentence', methods=["GET", "POST"])
def predict_sentence():
    if request.method == "GET":
        content = request.args.get('data')
        # print(content)
        sen, sen_list, negAns, posAns = predict(content)
        obj = {
            'sen': sen,
            'sen_list': sen_list,
            'negAns': negAns,
            'posAns': posAns
        }
        # print(obj)
        jsonobj = json.dumps(obj, indent=2, ensure_ascii=False, default=set_default)
        return jsonobj

    if request.method == "POST":
        print('post')
        return ' '


@app.route('/getChipin', methods=['POST'])
def getChipin_file():
    uploaded_file = request.files['file']
    content = uploaded_file.read().decode('utf-8')
    list_ = content.split('\r\n')
    words = []
    wds = Seg()
    for i in list_:
        i = re.sub(r"[!?！？]", '', i)
        words.append(wds.cut(i))
    result = []
    for w_list in words:
        for w in w_list:
            result.append(w)
    result = myUtils.getSentimentWords(result)
    uploaded_file.close()
    return json.dumps(result, indent=2, ensure_ascii=False)


@app.route('/getChipin_list', methods=['POST'])
def getChipin_list():
    # 这里接收的是一个list，每一项都是一个评论
    list_ = request.get_json()
    # print(list_)
    words = []
    wds = Seg()
    result = []
    for i in list_:
        i = re.sub(r"[!?！？]", '', i)
        words.append(wds.cut(i))
    for w_list in words:
        for w in w_list:
            result.append(w)
    # print(result)
    return json.dumps(myUtils.getSentimentWords(result), indent=2, ensure_ascii=False)


@app.route('/feedback', methods=['POST'])
def feedback():
    req = request.json
    data = req['data']
    sen = req['sen']
    if sen == '积极':
        sen = 1
    else:
        sen = 0
    # print(data_)
    with open('./feedback_data/feedback.txt', 'a', encoding='utf-8') as f:
        f.write(data + ' ' + str(sen) + '\n')
    return '成功接收反馈'


@app.route('/predata', methods=['GET'])
def predata_():
    if request.method == 'GET':
        content = request.args.get('data')
        res = Seg().cut(content)
        print(res)
        jsonobj = json.dumps(res, indent=2, ensure_ascii=False)
        return jsonobj


# 返回爬取到的评论数据给前端
@app.route('/spider', methods=['GET'])
def spider_():
    if request.method == 'GET':
        url = request.args.get('url')
        print(url)
        comment_list = spider(url)

        obj = {
            'info': '',
            'comment_data': comment_list,
        }

        return json.dumps(obj, indent=2, ensure_ascii=False)


@app.route('/register', methods=['POST'])
def register_():
    req = request.json
    print(req)
    account = req['account']
    password = req['password']

    conn = sqlite3.connect('./emtoin.db')
    cur = conn.cursor()
    sql1 = 'select account from user'
    res = cur.execute(sql1)
    # accountList = []
    for row in res:
        # accountList.append(row[0])
        if account == row[0]:
            conn.close()
            return '账号已经存在！'

    # if account in accountList:
    #     conn.close()
    #     return '账号已经存在！'

    sql2 = f'insert into user(account,password) values({account},{password})'
    cur.execute(sql2)
    conn.commit()
    conn.close()
    return '注册成功！'


@app.route('/login', methods=['POST'])
def login_():
    req = request.json
    account = req['account']
    password = req['password']

    conn = sqlite3.connect('./emtoin.db')
    cur = conn.cursor()
    sql1 = 'select account,password from user'
    acc = cur.execute(sql1)
    for row in acc:
        if account == row[0] and password == row[1]:
            conn.close()
            return 'true'
        if account == row[0] and password != row[1]:
            conn.close()
            return 'false'
    conn.close()
    return 'none'


if __name__ == '__main__':
    app.run()
