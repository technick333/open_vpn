from flask import Flask,jsonify,render_template
import socket as s
import re
import time
from  flask_bootstrap import Bootstrap
from  collections import defaultdict

FILE_STATUS = 'openvpn-status.log'

app  = Flask(__name__)
bootstrap = Bootstrap(app)


@app.route('/')
def index():
    return render_template('new_index.html')

#This it a comment 

@app.route('/get_status_new',methods = ['GET'])
def get_status_new():
    with open(FILE_STATUS,'r') as f:
        lines =  f.readlines()
        
        end_blck_clien_index  = lines.index('ROUTING TABLE\n')
        end_blck_routin_index = lines.index('GLOBAL STATS\n')
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
	app.run(host='localhost',port=5555)



