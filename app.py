from flask import Flask,jsonify,render_template
import socket as s
import re
import time
from  flask_bootstrap import Bootstrap
from  collections import defaultdict

app  = Flask(__name__)
bootstrap = Bootstrap(app)



def get_data():
    cli = s.socket(s.AF_INET,s.SOCK_STREAM)
    cli.connect(('127.0.0.1',7777))
    cli.recv(4096)
    cli.send('status 1\r\n')
    time.sleep(0.1)
    data = ''
    while True:
        buff = cli.recv(4096)
        data = data +buff
        if len(buff) < 4096 :break
    return data


@app.route('/')
def index():
    return render_template('new_index.html')


@app.route('/get_status_new',methods = ['GET'])
def get_new():
        lines = get_data().split('\r\n')
        end_blck_clien_index  = lines.index('ROUTING TABLE')
        end_blck_routin_index = lines.index('GLOBAL STATS')
        header  =lines[2].split(',')
        users = defaultdict(str)

        for item in lines[3:end_blck_clien_index]:
            user = dict((k.strip(),v.strip()) for (k,v) in zip(header,item.split(',')))
            users[user['Real Address']] = user

        header =lines[end_blck_clien_index+1].split(',')

        for item in lines[end_blck_clien_index+2:end_blck_routin_index]:
             user = dict((k.strip(),v.strip()) for (k,v) in zip(header,item.split(',')))
             users[user['Real Address']]['Virtual Address']=user['Virtual Address']
             users[user['Real Address']]['Last Ref'] = user['Last Ref']

        return jsonify({'users':users})



if __name__ =='__main__':
    app.run(host='0.0.0.0',port=5555,debug=True)

