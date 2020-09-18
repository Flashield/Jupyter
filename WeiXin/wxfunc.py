import time
import cx_Oracle

import wx_other_fun
from wx_param import *
from wxuser import WxUser

wx_users = dict()

def sms_msg(wx_get_msg):
    """发送短信提醒"""
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

def send_text_msg(text_msg):
    """发送文本文本信息"""

def sendmsg(send_msg):
    """发送xml格式回复消息"""
    CreateTime=int(time.time())
    print('send_msg:{}'.format(send_msg))
    if send_msg['MsgType'] == 'text':
        xml_msg = text_msg_format.format(
            send_msg['FromUserName'],send_msg['ToUserName'],CreateTime,
            send_msg['MsgType'],send_msg['Content'])
    return xml_msg

def deal_menu(wxuser, msg_input):
    """处理不同的菜单项"""
    if wxuser.menu == ['1']:
        pass
    elif wxuser.menu == ['4']:
        reply_text_content = wxuser.game_calc(msg_input)
    return reply_text_content

def deal_text_msg(deal_msg, wxuser):
    """处理文本消息"""
    reply_msg = dict()
    if wxuser.menu == []:
        if deal_msg['Content'] == 'help':
            reply_text_content = help_text_msg
        elif deal_msg['Content'] == '4':
            wxuser.menu.append('4')
            reply_text_content = '''进入四则运算，回复b开始出题，回复q退回至上一级菜单：''' 
        else:
            # 图灵机器人
            reply_text_content = wx_other_fun.msg_tuling_bot(deal_msg['Content'])
    else:
        reply_text_content = deal_menu(wxuser, deal_msg['Content'])
    reply_msg['MsgType'] = 'text'
    reply_msg['Content'] = reply_text_content
    reply_msg['FromUserName'] = deal_msg['ToUserName']
    reply_msg['ToUserName'] = deal_msg['FromUserName']
    return sendmsg(reply_msg)

def paser_msg(paser_data):
    """解析公众平台传入的数据"""
    msg = 'success'
    CreateTime = int(time.time())
    user_id = paser_data['FromUserName']
    if user_id not in wx_users.keys():
        wxuser = WxUser(user_id)
        wx_users[user_id] = wxuser
    if paser_data['MsgType'] == 'text':
        # 处理文字消息
        msg = deal_text_msg(paser_data, wx_users[user_id])
    elif paser_data['MsgType'] == 'image':
        # 处理图片消息
        words_ocr_result = wx_other_fun.baidu_gen_ocr_url(paser_data['PicUrl'])
        rply_msg = dict()
        rply_msg['FromUserName'] = paser_data['ToUserName']
        rply_msg['ToUserName'] = paser_data['FromUserName']
        rply_msg['MsgType'] = 'text'
        rply_msg['Content'] = words_ocr_result.replace('<','') #有<，无法正常接收
        msg = sendmsg(rply_msg)
    elif paser_data['MsgType'] == 'voice':
        # 处理语音消息
        msg  = voice_msg_format.format(
            paser_data['ToUserName'],paser_data['FromUserName'],
            paser_data['CreateTime'],paser_data['MsgType'],paser_data['MediaId'])
    elif paser_data['MsgType'] == 'event' and paser_data['Event'] == 'subscribe':
        reply_content = '欢迎关注闪盾的微信公众号，简单功能：\n随便和我聊聊，我还会做算术题哦。\n获取详细帮助信息请回复:help。'
        msg = text_msg_format.format(
            paser_data['ToUserName'],paser_data['FromUserName'],CreateTime,
            'text',reply_content)
    else:
        msg = 'success'
    return msg