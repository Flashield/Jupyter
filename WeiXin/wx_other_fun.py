import urllib
import urllib.request
import json
import base64
import time

#tuling_apikey = '6cf4f224dee642b2b55a89d2638fa982' #找不到用户名和密码了
tuling_apikey = '6228551539264e05b49bad59b88a5918'

baidu_api_key = 'BCAwnGO4F52VzHEFqN4MfGtO'
baidu_sec_key = 'xAeNmX1UxslHKvOC4gmyY3bQya5P49FX'

def msg_tuling_bot(chat_request):
    chatbot_url = 'http://openapi.tuling123.com/openapi/api/v2'
    post_dict = {'reqType':'0',
       'perception': {'inputText': {'text': ''},
                      'inputImage': {'url': 'imageUrl'},
                      'selfInfo': {'location': {'city': '南通', 'province': '江苏', 'street': '洪江路'}}},
      'userInfo': {'apiKey': '', 'userId': 'Flashield'}}
    post_dict['perception']['inputText']['text']=chat_request
    post_dict['userInfo']['apiKey']=tuling_apikey
    post_data=json.dumps(post_dict).encode('UTF-8')
    opener = urllib.request.build_opener()
    request = opener.open(chatbot_url,post_data)
    req_text = request.read().decode(encoding='UTF8',errors='ignore')
    reply = json.loads(req_text)
    reply_text = reply['results'][0]['values']['text']
    return reply_text

def get_baidu_access_token():
    access_token=dict()
    with open('cfg_file.cfg','r') as cfg_file:
        access_token = eval(cfg_file.readlines()[0])
    if access_token['live_time'] < int(time.time()):
        #access_token过期后，重新获取
        acc_token_url = 'https://aip.baidubce.com/oauth/2.0/token'
        opener = urllib.request.build_opener()
        data = {"grant_type":"client_credentials", "client_id":baidu_api_key, "client_secret":baidu_sec_key}
        post_data = urllib.parse.urlencode(data).encode(encoding='UTF8')
        request = opener.open(acc_token_url,post_data)
        html = request.read().decode(encoding='UTF8',errors='ignore')
        acc_token = json.loads(html)
        access_token['baidu_ai_access_token'] = acc_token['access_token']
        access_token['live_time'] = int(time.time())+acc_token['expires_in']-3600
        with open('cfg_file.cfg','w') as cfg_file:
            cfg_file.write(str(access_token))
    return access_token

def baidu_gen_ocr_url(PicUrl):
    access_token = get_baidu_access_token()
    gen_ocr_url = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token={}'.format(access_token['baidu_ai_access_token'])
    headers = [('Content-Type','application/x-www-form-urlencoded'),]
    opener = urllib.request.build_opener()
    opener.addheaders = headers
    data={'url':PicUrl}
    post_data = urllib.parse.urlencode(data).encode(encoding='UTF8')
    request = opener.open(gen_ocr_url,post_data)
    html = request.read().decode(encoding='UTF8',errors='ignore')
    result = json.loads(html)
    words_result= ''
    for words in result['words_result']:
        words_result += '{}\n'.format(words['words'])
    return words_result