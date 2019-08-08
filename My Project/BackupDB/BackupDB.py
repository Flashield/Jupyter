import cx_Oracle
import os
import time
import logging

bakctrluser='NTBACKUP'
bakctrlpass='NTBACKUP'
bakctrldb='ESXVM0504'
baklocdir='/file/NTBak'
ldspe='/'
logFile=baklocdir+ldspe+'log'+ldspe+'backup'+time.strftime('%Y%m%d%H%M%S')+'.log'

def initLog():
    logger=logging.getLogger()
    logHandler=logging.FileHandler(logFile)
    print(logFile)
    logfmter=logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    logHandler.setFormatter(logfmter)
    logger.addHandler(logHandler)
    logger.setLevel(logging.INFO)
    return logger

def DB_Back_Deal(dbbak):
    dbbakname=dbbak[0]
    dbbakuser=dbbak[1]
    dbbakpass=dbbak[2]
    dbbakschema=dbbak[3]
    dbbaktab=dbbak[4]
    dbbakispar=dbbak[5]
    dbbakndtrunc=dbbak[6]
    if dbbakschema==1:
        DB_Back_Schema(dbbakname,dbbakuser,dbbakpass)
    else:
        if dbbakispar==0:
            DB_Back_Table(dbbakname,dbbakuser,dbbakpass,dbbaktab)
        else:
            if dbbakispar==1:
                DB_Back_Partition(dbbakname,dbbakuser,dbbakpass,dbbaktab)
            else:
                logger.warning("Wrong Parameters!")

def DB_Back_Schema(dbname,dbuser,dbpass):
    s_path=baklocdir+ldspe+dbname+ldspe+dbuser
    s_filename_suff=dbuser+'_'+time.strftime('%Y%m%d')
    try:
        os.makedirs(s_path)
    except:
        print('Directory Exists')
    s_cmd='exp '+dbuser+'/'+dbpass+'@'+dbname+' file='+s_path+ldspe+s_filename_suff+'.dmp buffer=1048576'
    logger.info(s_cmd)
    os.system(s_cmd)
    s_cmd='rar a -df -ep '+s_path+ldspe+s_filename_suff+' '+s_path+ldspe+s_filename_suff+'.dmp'
    logger.info(s_cmd)
    os.system(s_cmd)
    
def DB_Back_Table(dbname,dbuser,dbpass,dbtab):
    s_path=baklocdir+ldspe+dbname+ldspe+dbuser
    s_filename_suff=dbuser+'_'+dbtab+'_'+time.strftime('%Y%m%d')
    try:
        os.makedirs(s_path)
    except:
        print('Directory Exists')
    s_cmd='exp '+dbuser+'/'+dbpass+'@'+dbname+' tables='+dbtab+' file='+s_path+ldspe+s_filename_suff+'.dmp buffer=1048576'
    logger.info(s_cmd)
    os.system(s_cmd)
    s_cmd='rar a -df -ep '+s_path+ldspe+s_filename_suff+' '+s_path+ldspe+s_filename_suff+'.dmp'
    logger.info(s_cmd)
    os.system(s_cmd)
    
def DB_Back_Partition(dbname,dbuser,dbpass,dbtab):
    s_path=baklocdir+ldspe+dbname+ldspe+dbuser+ldspe+dbtab
    s_filename_suff=dbuser+'_'+dbtab+time.strftime('%Y%m%d')
    try:
        os.makedirs(s_path)
    except:
        print('Directory Exists')
    dbconn=cx_Oracle.connect(dbuser,dbpass,dbname)
    dbcur=dbconn.cursor()
    dbcur.execute('SELECT * FROM user_tab_partitions a \
    JOIN user_segments b ON a.table_name=b.segment_name AND a.partition_name=b.partition_name \
    WHERE a.table_name=:1 AND b.bytes>b.initial_extent \
    ORDER BY a.partition_name',(dbtab,))
    dbrlt=dbcur.fetchall()
    for j in dbrlt:
        s_cmd = 'exp '+dbuser+'/'+dbpass+'@'+dbname+' tables='+j[0]+':'+j[2]+' file='+s_path+ldspe+j[0]+'_'+j[2]+'.dmp buffer=1048576'
        logger.info(s_cmd)
        os.system(s_cmd)
        s_cmd = 'rar a -df -ep '+s_path+ldspe+j[0]+'_'+j[2]+' '+s_path+ldspe+j[0]+'_'+j[2]+'.dmp'
        logger.info(s_cmd)
        os.system(s_cmd)

def DB_Update(dbbak,deal_type):
    bakctrlconn=cx_Oracle.connect(bakctrluser,bakctrlpass,bakctrldb)
    if deal_type=='BDATE':
        deal_cur=bakctrlconn.cursor()
        deal_cur.execute('UPDATE db_backup_ctrl a SET a.deal_bak_bdate = SYSDATE \
        WHERE a.db_name=:1 AND a.db_user=:2 AND a.db_pass=:3 AND a.rowid=:4 AND a.deal_bak_bdate IS NULL',(dbbak[0],dbbak[1],dbbak[2],dbbak[10]))
        bakctrlconn.commit()
        deal_cur.close()
    else:
        if deal_type=='EDATE':
            deal_cur=bakctrlconn.cursor()
            deal_cur.execute('UPDATE db_backup_ctrl a SET a.deal_bak_edate = SYSDATE \
            WHERE a.db_name=:1 AND a.db_user=:2 AND a.db_pass=:3 AND a.rowid=:4 AND a.deal_bak_edate IS NULL',(dbbak[0],dbbak[1],dbbak[2],dbbak[10]))
            bakctrlconn.commit()
            deal_cur.close()
    bakctrlconn.close()

logger=initLog()
logger.info('Backup Start .....')

try:
    bakctrlconn=cx_Oracle.connect(bakctrluser,bakctrlpass,bakctrldb)
    bakctrlcur=bakctrlconn.cursor()
    bakctrlcur.execute('SELECT a.*,a.rowid FROM db_backup_ctrl a \
    WHERE a.deal_bak_bdate IS NULL AND a.need_bak_date<SYSDATE')
    bakctrlrlt=bakctrlcur.fetchall()
    bakctrlcur.close()
    bakctrlconn.close()
        
    for i in bakctrlrlt:
        #print i
        DB_Update(i,'BDATE')
        DB_Back_Deal(i)
        DB_Update(i,'EDATE')
    
    logger.info('Backup Ended!')
except Exception as ex:
    logger.error(ex+' Program End Abnormailly')
