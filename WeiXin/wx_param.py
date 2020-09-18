voice_msg_format = '''<xml>
        <FromUserName>{}</FromUserName>
        <ToUserName>{}</ToUserName>
        <CreateTime>{}</CreateTime>
        <MsgType>{}</MsgType>
        <Voice>
        <MediaId>{}</MediaId>
        <Voice>
        </xml>'''

text_msg_format = '''<xml>
        <FromUserName>{}</FromUserName>
        <ToUserName>{}</ToUserName>
        <CreateTime>{}</CreateTime>
        <MsgType>{}</MsgType>
        <Content>{}</Content>
        </xml>'''

help_text_msg = '''帮助信息：\n 
1、回复文字消息，公众号会和你聊天，还会算算术哦！\n
2、回复图片消息，公众号会识别出里面的文字哦！\n
3、回复数字4，公众号会给你出四则运算题目哦！'''