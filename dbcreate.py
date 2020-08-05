#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 17:30:06 2020

@author: emilykuo
"""
#============================================================================
# 歷史資料寫入資料庫
import pandas as pd

h106=pd.read_csv(r'/Users/emilykuo/Desktop/實價登錄/afterwash/house106.csv',index_col=0)
h107=pd.read_csv(r'/Users/emilykuo/Desktop/實價登錄/afterwash/house107.csv',index_col=0)
h108=pd.read_csv(r'/Users/emilykuo/Desktop/實價登錄/afterwash/house108.csv',index_col=0)
h109=pd.read_csv(r'/Users/emilykuo/Desktop/實價登錄/afterwash/house109.csv',index_col=0)

columns=h106.columns
columnssr=pd.Series(columns)

# 1. 設定欄位與其格式
for x in range(28):
    if x == 3 or x== 15 or x==24:
        columnssr[x]=columnssr[x]+" REAL"
    elif x ==7 or x == 14 or x == 16 or x == 17 or x == 18 or x == 21 or x == 22 or x == 25:
        columnssr[x]=columnssr[x]+" INTEGER"
    else:
        columnssr[x]=columnssr[x]+" TEXT"

head=""
for x in range(28):
    if x==27:
        head+=columnssr[x]
    else:
        head+=columnssr[x]+"," 

head1=head.replace("-","")
#====================================================================
# 2. 資料預處理
h106r=h106.fillna("NULL")
h107r=h107.fillna("NULL")
h108r=h108.fillna("NULL")
h109r=h109.fillna("NULL")

#====================================================================
# 3. 寫入資料庫
import pandas as pd
import sqlite3
print(len(h106))
conn = sqlite3.connect ("python_project.db") #連接資料庫
sql="CREATE TABLE house106 ("+head1+")"
new = conn.execute(sql) #執行SQL命令
for x in range(len(h106r)):
    rowdata=str(tuple(h106r.loc[x]))
    sqldata="INSERT INTO house106 VALUES"+rowdata
    newdata=conn.execute(sqldata)
conn.commit()

sql="CREATE TABLE house107 ("+head1+")"
new = conn.execute(sql) #執行SQL命令
for x in range(len(h107r)):
    rowdata=str(tuple(h107r.loc[x]))
    sqldata="INSERT INTO house107 VALUES"+rowdata
    newdata=conn.execute(sqldata)
conn.commit()

sql="CREATE TABLE house108 ("+head1+")"
new = conn.execute(sql) #執行SQL命令
for x in range(len(h108r)):
    rowdata=str(tuple(h108r.loc[x]))
    sqldata="INSERT INTO house108 VALUES"+rowdata
    newdata=conn.execute(sqldata)
conn.commit()

sql="CREATE TABLE house109 ("+head1+")"
new = conn.execute(sql) #執行SQL命令
for x in range(len(h109r)):
    rowdata=str(tuple(h109r.loc[x]))
    sqldata="INSERT INTO house109 VALUES"+rowdata
    newdata=conn.execute(sqldata)
conn.commit() #確認交易
conn.close() #資料庫關閉
#===============================================================================
























