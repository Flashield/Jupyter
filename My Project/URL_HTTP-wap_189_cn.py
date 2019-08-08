
import urllib
import urllib.request
import http
import http.cookiejar
import cx_Oracle
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

spider='wapjs_esxvm2208'
spider_db_user='NTTASK'
spider_db_pass='NTTASK'
spider_db='ESXVM0504'

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1024x768")
browser = webdriver.Chrome(options=chrome_options)
browser.get("http://wapjs.189.cn/tysh/pages/kdSpeedUp/speedUpIndexNew.html")


def get_kdinfo(En_CertID):
    url = 'http://wapjs.189.cn/zt-business/broadBandBuiness/selectUserBroadAccNbr'
    opener = urllib.request.build_opener()
    #添加headers
    headers = [('Referer','http://wapjs.189.cn/tysh/pages/kdSpeedUp/speedUpIndexNew.html?ztInterSource=300177&platform=wap&callback=252133'),               ('Accept-Language','zh-CN;q=0.8,zh;q=0.6,en-US;q=0.4'),               ('Cache-Control','max-age=0'),               ('Content-Type','application/x-www-form-urlencoded'),               ('Origin',url),               ('Connection','keep-alive'),               ('User-Agent','Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'),               ('Accept','application/json, text/javascript, */*; q=0.01')]
    opener.addheaders = headers

    #添加cookie
    cookie_filename = 'wap_cookie_189_cn.txt'
    #cookies = http.cookiejar.CookieJar()
    cookies = http.cookiejar.MozillaCookieJar(cookie_filename)
    cookies.load(ignore_discard=True, ignore_expires=True)
    change_cookie = http.cookiejar.Cookie(
        version=0, name="cityCode", value="js_nt",
        port=None, port_specified=False,
        domain="js.189.cn",
        domain_specified=True, domain_initial_dot=False,
        path="/", path_specified=True, secure=False,
        expires=None, discard=True,
        comment=None, comment_url=None,
        rest={"HttpOnly": None}, rfc2109=False)
    #cookies.set_cookie(change_cookie)
    cookie_handler = urllib.request.HTTPCookieProcessor(cookies)
    opener.add_handler(cookie_handler)
    #添加代理
    proxy_handler = urllib.request.ProxyHandler({'https':'221.178.146.113:61388','http':'221.178.146.113:61388'})
    #opener.add_handler(proxy_handler)

    data = {"para":En_CertID}
    post_data = urllib.parse.urlencode(data).encode(encoding='UTF8')
    #print(post_data)
    try:
        request = opener.open(url,post_data)
        kd_info=request.read().decode(encoding='utf8',errors='ignore')
    except Exception as ex:
        print(ex)
        kd_info='Exception!'
    return kd_info

while True:
    dbconn=cx_Oracle.connect(spider_db_user,spider_db_pass,spider_db)
    dbcur=dbconn.cursor()
    smt_sql = "UPDATE kd_dx_customer a SET a.spider_source = '{}' WHERE a.certid like '3206%' AND a.spider_source IS NULL AND ROWNUM <= 2".format(spider)
    dbcur.execute(smt_sql)
    dbconn.commit()
    smt_sql = "SELECT a.certid FROM kd_dx_customer a WHERE a.spider_source = '{}' AND a.kd_info IS NULL".format(spider)
    dbcur.execute(smt_sql)
    dbrlt=dbcur.fetchall()
    for CertInfo in dbrlt:
        print(CertInfo[0])
        Plain_PostData="accountType=2;idCard={};areaCode=0513;actionCode=jsztActionCode_mallbroadBandBuinessselectUserBroadAccNbr;PathCode=mall-00003;channelCode_common=300177;pubAreaCode=025;pushUserId=jszt_912507;coachUser=;userLogAccNbrType=;userLogAccNbr=;userTokenAccNbrType=2;ztVersion=4.0;ztInterSource=300177;pubToken=undefined;".format(CertInfo[0])
        print(Plain_PostData)
        time.sleep(30)
        En_CertID = browser.execute_script('return ztEncrptyUtil.encode("{}")'.format(Plain_PostData))
        print(En_CertID)
        DX_kd_info=get_kdinfo(En_CertID)        
        print(DX_kd_info)
        smt_sql = "update kd_dx_customer a SET a.kd_info='{}',a.check_time=SYSDATE WHERE a.certid = '{}' AND a.spider_source = '{}'".format(DX_kd_info,CertInfo[0],spider)
        dbcur.execute(smt_sql)
        dbconn.commit()
    dbcur.close()
    dbconn.close()
#print(dbrlt)
