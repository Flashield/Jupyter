#!/bin/sh
#ORACLE_BASE=/usr/app/oracle;export ORACLE_BASE
#ORACLE_HOME=$ORACLE_BASE/920;export ORACLE_HOME
#ORACLE_SID=ntbak;export ORACLE_SID
#LD_LIBRARY_PATH=$ORACLE_HOME/lib; export LD_LIBRARY_PATH
#ORACLE_OEM_JAVARUNTIME=/usr/local/jre1.3.1_19; export ORACLE_OEM_JAVARUNTIME
#PATH=/usr/local/bin:/usr/sbin:$ORACLE_HOME/bin:$PATH;export PATH
umask 0002

PATH=$PATH:$HOME/bin:/usr/lib/oracle/instantclient
SQLPATH=/usr/lib/oracle/instantclient
TNS_ADMIN=/usr/lib/oracle/instantclient/network
NLS_LANG="SIMPLIFIED CHINESE_CHINA.ZHS16GBK"
#PKG_CONFIG_PATH=/usr/local/lib/pkgconfig:$PKG_CONFIG_PATH
LD_LIBRARY_PATH=$SQLPATH
LD_LIBRARY_PATH=$SQLPATH:$LD_LIBRARY_PATH

export PATH
export SQLPATH TNS_ADMIN NLS_LANG LD_LIBRARY_PATH #PKG_CONFIG_PATH


python3 /home/ntbackup/BackupDB.py
