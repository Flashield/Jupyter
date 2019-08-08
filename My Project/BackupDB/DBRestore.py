import os
from SendSMS import sms_send
import string

FromDB='NTDB'
FromUser='NTDSS'
FromDir='BS_CDR_GSM_LOC_201208'
ToDB='NTDB05'
ToUser='NTHISTORY'
ToPass='NTHISTORY'

RestoreTable='BS_CDR_GSM_LOC_201208'
for day_number in range(3,32):
    RestorePartitionPre='P_BS_CDR_'
    for RestoreCounty in range(3,4):
        #RestoreCounty='03'
        RestorePartition=RestorePartitionPre+string.zfill(day_number,2)+'_'+string.zfill(RestoreCounty,2)
        RestorePartition2=RestorePartitionPre+string.zfill(day_number,2)
        baklocdir='/var/ftp/NTBak'
        ldspe='/'
    
        fileDir=baklocdir+ldspe+FromDB+ldspe+FromUser+ldspe+FromDir+ldspe
        filename=RestoreTable+'_'+RestorePartition
        filename2=RestoreTable+'_'+string.zfill(day_number,2)+'_'+string.zfill(RestoreCounty,2)
        fileExname=fileDir+filename
        fileExname2=fileDir+filename2
        s_cmd='unrar x '+fileExname2+'.rar'
        print s_cmd
        os.system(s_cmd)
        s_cmd='imp '+ToUser+'/'+ToPass+'@'+ToDB+' file='+filename2+'.dmp fromuser='+FromUser+' '+'touser='+ToUser+' ignore=y buffer=1048576'
        print s_cmd 
        os.system(s_cmd)
        s_cmd='rm '+filename2+'.dmp'
        print s_cmd
        os.system(s_cmd)

sms_send('13806296955', '4', 'Import Finished, Check it')
