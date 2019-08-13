# To add a new cell, type '#%%'
# To add a new markdown cell, type '#%% [markdown]'
#%% Change working directory from the workspace root to the ipynb file location. Turn this addition off with the DataScience.changeDirOnImportExport setting
# ms-python.python added
import os
try:
	os.chdir(os.path.join(os.getcwd(), 'Jupyter/My Project/.ipynb_checkpoints'))
	print(os.getcwd())
except:
	pass

#%%
import urllib
import urllib.request
import http
import http.cookiejar
import cx_Oracle
import time


#%%
spider='esxvm2208'
spider_db_user='NTTASK'
spider_db_pass='NTTASK'
spider_db='ESXVM0504'


#%%
while True:
    dbconn=cx_Oracle.connect(spider_db_user,spider_db_pass,spider_db)
    dbcur=dbconn.cursor()
    smt_sql = "UPDATE kd_dx_customer a SET a.spider_source = '{}' WHERE a.certid like '3206%' AND a.spider_source IS NULL AND ROWNUM <= 100".format(spider)
    dbcur.execute(smt_sql)
    dbconn.commit()
    smt_sql = "SELECT a.certid FROM kd_dx_customer a WHERE a.spider_source = '{}' AND a.kd_info IS NULL".format(spider)
    dbcur.execute(smt_sql)
    dbrlt=dbcur.fetchall()
    for CertInfo in dbrlt:
        print(CertInfo[0])
        DX_kd_info=get_kdyinfo(CertInfo[0])
        time.sleep(2)
        print(DX_kd_info)
        smt_sql = "update kd_dx_customer a SET a.kd_info='{}',a.check_time=SYSDATE WHERE a.certid = '{}' AND a.spider_source = '{}'".format(DX_kd_info,CertInfo[0],spider)
        dbcur.execute(smt_sql)
        dbconn.commit()
    dbcur.close()
    dbconn.close()
#print(dbrlt)


#%%
def get_kdyinfo(ID):
    url = 'http://www.kuaidi.com/kuaidiyuan/{}.html'.format(ID)
    opener = urllib.request.build_opener()
    #添加headers
    headers = [('Referer','http://js.189.cn/umall/broadbandExtend/index'),               ('Accept-Language','zh-CN;q=0.8,zh;q=0.6,en-US;q=0.4'),               ('Cache-Control','max-age=0'),               ('Content-Type','application/x-www-form-urlencoded'),               ('Origin',url),               ('Connection','keep-alive'),               ('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'),               ('Accept','application/json, text/javascript, */*; q=0.01')]
    opener.addheaders = headers

    #添加cookie
    cookie_filename = 'cookie_189_cn.txt'
    #cookies = http.cookiejar.CookieJar()
    #cookies = http.cookiejar.MozillaCookieJar(cookie_filename)
    #cookies.load(ignore_discard=True, ignore_expires=True)
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
    #cookie_handler = urllib.request.HTTPCookieProcessor(cookies)
    #opener.add_handler(cookie_handler)
    #添加代理
    proxy_handler = urllib.request.ProxyHandler({'https':'221.178.146.113:61388','http':'221.178.146.113:61388'})
    #opener.add_handler(proxy_handler)

    #添加PostData
    #data = {"accNbr":"32062519621126691X","areaCode":"0513","isIdCard":"1"}
    #data = {"accNbr":CertID,"areaCode":"0513","isIdCard":"1"}
    #post_data = urllib.parse.urlencode(data).encode(encoding='UTF8')
    #print(post_data)
    try:
        request = opener.open(url)
        kdy_detail=request.read().decode(encoding='utf8',errors='ignore')
        kdy=[kdy_info[kdy_info.find('联系电话')+36:kdy_info.find('联系电话')+47],kdy_info[kdy_info.find('所属区域'):kdy_info.find('所属区域')+120]]
    except Exception as ex:
        kdy=['Exception!'+str(ex),'Exception!']
    return kdy


#%%
dbconn=cx_Oracle.connect(spider_db_user,spider_db_pass,spider_db)
dbcur=dbconn.cursor()
for kdy_id in range(74190,78190):
    kdy_info = get_kdyinfo(kdy_id)
    smt_sql = "INSERT INTO t_kuaidiyuan_info(kdy_msisdn,kdy_district) VALUES('{}','{}')".format(kdy_info[0],kdy_info[1])
    dbcur.execute(smt_sql)
    dbconn.commit()
dbcur.close()
dbconn.close()    


#%%
url = 'http://www.kuaidi.com/kuaidiyuan/{}.html'.format(74190)


#%%
opener = urllib.request.build_opener()
headers = [('Referer','http://js.189.cn/umall/broadbandExtend/index'),           ('Accept-Language','zh-CN;q=0.8,zh;q=0.6,en-US;q=0.4'),           ('Cache-Control','max-age=0'),           ('Content-Type','application/x-www-form-urlencoded'),           ('Origin',url),           ('Connection','keep-alive'),           ('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0'),           ('Accept','application/json, text/javascript, */*; q=0.01')]
opener.addheaders = headers


#%%
request = opener.open(url)


#%%
kdy_info=request.read().decode(encoding='utf8',errors='ignore')


#%%
get_kdyinfo(74191)


#%%
kdy_info[kdy_info.find('所属区域'):kdy_info.find('所属区域')+120]


#%%
kdy_info[kdy_info.find('联系电话')+36:kdy_info.find('联系电话')+47]


#%%
kdy=[kdy_info[kdy_info.find('联系电话')+36:kdy_info.find('联系电话')+47],kdy_info[kdy_info.find('所属区域'):kdy_info.find('所属区域')+120]]


#%%
kdy_info[kdy_info.find('联系电话')-20:kdy_info.find('联系电话')]


