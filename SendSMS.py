import cx_Oracle
import os
import sys

sms_db = 'esxvm0504'
sms_db_user = 'ntsms'
sms_db_password = 'smsinterface'

def sms_send(v_msisdn,v_actid,v_message):
    sms_conn=cx_Oracle.connect('ntsms','smsinterface','esxvm0504')
    sms_cur=sms_conn.cursor()    
    sms_cur.callproc('p_send_sms',[v_msisdn,v_actid,v_message])
    print('Message send to '+v_msisdn+': '+v_message)
    sms_cur.close()
    sms_conn.close()    

if len(sys.argv)==4:
    sms_msisdn=sys.argv[1]
    sms_act_id=sys.argv[2]
    sms_message=sys.argv[3]
    sms_send(sms_msisdn,sms_act_id,sms_message)
else:
    print('Argument Error, Check it!')
