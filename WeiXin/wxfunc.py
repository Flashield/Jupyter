import time
import wx_other_fun
import cx_Oracle

def sms_msg(wx_get_msg):
    dbconn=cx_Oracle.connect('NTTask','NTTask','ESXVM0504')
    dbcur = dbconn.cursor()
    proc_data = 'Message from Weixin:{}'.format(wx_get_msg)
    dbcur.callproc('Weixin_Msg',[proc_data,])
    dbcur.close()
    dbconn.close()

def parse_xml(data):
    try:
        import xml.etree.cElementTree as ET
    except ImportError:
        import xml.etree.ElementTree as ET
    get_data = dict()
    root = ET.fromstring(data)
    for child in root:
        get_data[child.tag] = child.text
    datas = paser_msg(get_data)
    print("datas:{}".format(datas))
    return datas

def sendmsg(send_msg):
    CreateTime=int(time.time())
    print('send_msg:{}'.format(send_msg))
    if send_msg['MsgType'] == 'text':
        xml_msg = '''<xml>
        <FromUserName>{}</FromUserName>
        <ToUserName>{}</ToUserName>
        <CreateTime>{}</CreateTime>
        <MsgType>{}</MsgType>
        <Content>{}</Content>
        </xml>'''.format(send_msg['FromUserName'],send_msg['ToUserName'],CreateTime,\
                         send_msg['MsgType'],send_msg['Content'])
    return xml_msg

def deal_text_msg(deal_msg):
    reply_msg = dict()
    if deal_msg['Content'] == 'help':
        reply_content = '''帮助信息：\n1、回复文字消息，公众号会和你聊天，还会算算术哦！'''
        reply_msg['MsgType'] = 'text'
        reply_msg['Content'] = reply_content
    else:
        #图灵机器人
        reply_content = wx_other_fun.msg_tuling_bot(deal_msg['Content'])
        reply_msg['MsgType'] = 'text'
        reply_msg['Content'] = reply_content
    reply_msg['FromUserName'] = deal_msg['ToUserName']
    reply_msg['ToUserName'] = deal_msg['FromUserName']
    return sendmsg(reply_msg)

def paser_msg(paser_data):
    msg = 'success'
    CreateTime = int(time.time())
    if paser_data['MsgType'] == 'text':
        msg = deal_text_msg(paser_data)
    elif paser_data['MsgType'] == 'image':
        words_ocr_result = wx_other_fun.baidu_gen_ocr_url(paser_data['PicUrl'])
        rply_msg = dict()
        rply_msg['FromUserName'] = paser_data['ToUserName']
        rply_msg['ToUserName'] = paser_data['FromUserName']
        rply_msg['MsgType'] = 'text'
        rply_msg['Content'] = words_ocr_result.replace('<','') #有<，无法正常接收
        msg = sendmsg(rply_msg)
        #msg = '''<xml>
        #<FromUserName>{}</FromUserName>
        #<ToUserName>{}</ToUserName>
        #<CreateTime>{}</CreateTime>
        #<MsgType>{}</MsgType>
        #<PicUrl>{}</PicUrl>
        #<MsgId>{}</MsgId>
        #<Image>
        #<MediaId>{}</MediaId>
        #<Image>
        #</xml>'''.format(paser_data['ToUserName'],paser_data['FromUserName'],paser_data['CreateTime'],\
        #                 paser_data['MsgType'],paser_data['PicUrl'],paser_data['MsgId'],paser_data['MediaId'])
    elif paser_data['MsgType'] == 'voice':
        msg = '''<xml>
        <FromUserName>{}</FromUserName>
        <ToUserName>{}</ToUserName>
        <CreateTime>{}</CreateTime>
        <MsgType>{}</MsgType>
        <Voice>
        <MediaId>{}</MediaId>
        <Voice>
        </xml>'''.format(paser_data['ToUserName'],paser_data['FromUserName'],paser_data['CreateTime'],\
                         paser_data['MsgType'],paser_data['MediaId'])
    elif paser_data['MsgType'] == 'event' and paser_data['Event'] == 'subscribe':
        reply_content = '欢迎关注闪盾的微信公众号，简单功能：\n随便和我聊聊，我还会做算术题哦。\n获取详细帮助信息请回复:help。'
        msg = '''<xml>
        <FromUserName>{}</FromUserName>
        <ToUserName>{}</ToUserName>
        <CreateTime>{}</CreateTime>
        <MsgType>text</MsgType>
        <Content>{}</Content>
        </xml>'''.format(paser_data['ToUserName'],paser_data['FromUserName'],CreateTime,reply_content)
    else:
        msg = 'success'
    return msg