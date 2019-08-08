# coding:utf-8
from hashlib import sha1
from flask import Flask, request
import time
import urllib.request
import json
import wxfunc

token = 'Flashield'
appid = 'wx52d8b7b32451e895'
appsec = 'fb9eeaf21b92ceed9b8200c44fabea6d'
AccessToken = {'access_token': '12_46y9bFrNQlGBfJV1XkYMrrIc_Ab55sB0KZaYngky7dnUIZsx_40b50HSwzJry-ii7yvpaYWVgoF9Pnd_oT6V6EOJcUt1nFRiPbCpUJD1UibSVUaUftHDm80Tksjw2lhRoTMgCaLUEQH6k4vQDHPgAFALPX', 'live_time': 1534768234}

app = Flask(__name__)

def get_token(appid,appsec):
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}'.format(appid,appsec)    
    if int(AccessToken['live_time']) < int(time.time()):
        opener = urllib.request.build_opener()
        request = opener.open(url)
        get_acc_token = request.read().decode(encoding='UTF8',errors='ignore')
        AccessToken['access_token'] = json.loads(get_acc_token)['access_token']
        AccessToken['live_time'] = int(time.time())+json.loads(get_acc_token)['expires_in']-60
    print(AccessToken['access_token'],AccessToken['live_time'])
    return AccessToken['access_token']

def get_update(token, timestamp, nonce):
    arguments = ''
    for k in sorted([token, timestamp, nonce]):
        arguments = arguments + str(k)
    m = sha1()
    m.update(arguments.encode('utf8'))
    return m.hexdigest()

def check_signature():
    signature = request.args.get('signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    print(signature)
    check = get_update(token, timestamp, nonce)
    return True if check == signature else False



@app.route('/wx', methods=['GET', 'POST'])
def weixinInterface():
    if check_signature:
        if request.method == 'GET':
            echostr = request.args.get('echostr', '')
            return echostr
        elif request.method == 'POST':
            data = request.data
            print("data from Weixin:{}".format(data))
            msg = wxfunc.parse_xml(data)
            get_token(appid,appsec)
        return msg
    else:
        return 'signature error'
    
@app.route('/')
def index():
    return ""

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=9999,debug=True)