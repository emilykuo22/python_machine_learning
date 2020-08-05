#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 09:18:20 2020

@author: emilykuo
"""
import pandas as pd
import numpy as np
h061=pd.read_csv(r'/Users/emilykuo/Desktop/實價登錄/F_lvr_land_A106S1.csv',index_col=1)
h062=pd.read_csv(r'/Users/emilykuo/Desktop/實價登錄/F_lvr_land_A106S2.csv',index_col=1)
h063=pd.read_csv(r'/Users/emilykuo/Desktop/實價登錄/F_lvr_land_A106S3.csv',index_col=1)
h064=pd.read_csv(r'/Users/emilykuo/Desktop/實價登錄/F_lvr_land_A106S4.csv',index_col=1)

h061.reset_index(drop=False, inplace=True) 
h061=h061.drop(index=0,axis=0)
h062.reset_index(drop=False, inplace=True) 
h062=h062.drop(index=0,axis=0)
h063.reset_index(drop=False, inplace=True) 
h063=h063.drop(index=0,axis=0)
h064.reset_index(drop=False, inplace=True) 
h064=h064.drop(index=0,axis=0)

hall06=pd.concat([h061,h062,h063,h064])
hall06.reset_index(drop=True, inplace=True)

import re
building=[]
for h in hall06['交易筆棟數'][:]:
    match = re.search('建物\d+', h)
    match = match.group()
    building.append(int(match[2:]))
hall06['建物棟數']=building
msk=hall06['建物棟數']!=0
h106f=hall06[msk]
mskuse=h106f['主要用途'] == '住家用'
h106ff=h106f[mskuse]

h106ff= h106ff.drop(columns=['土地移轉總面積平方公尺', '都市土地使用分區', '非都市土地使用分區',
                    '非都市土地使用編定','交易筆棟數', '移轉層次', '總樓層數', 
                    '主要建材','建物現況格局-廳', '建物現況格局-衛','建物現況格局-隔間',
                    '車位類別', '車位移轉總面積平方公尺', '車位總價元','編號'])

h106ff=h106ff.dropna(subset=['單價元平方公尺'])
h106ff["建築完成年月"]=h106ff["建築完成年月"].fillna("0500101")

mskb=h106ff['建物型態']!='其他'
h106fff=h106ff[mskb]
mskc=h106fff['建物型態']!='廠辦'
h106ffff=h106fff[mskc]

# 行政區轉數字
dcdict={220:'板橋區',221:'汐止區',222:'深坑區',223:'石碇區',224:'瑞芳區',207:'萬里區',
208:'金山區',226:'平溪區',227:'雙溪區',228:'貢寮區',231:'新店區',232:'坪林區',233:'烏來區',234:'永和區',
235:'中和區',236:'土城區',237:'三峽區',238:'樹林區',239:'鶯歌區',241:'三重區',242:'新莊區',
243:'泰山區',244:'林口區',247:'蘆洲區',248:'五股區',249:'八里區',251:'淡水區',252:'三芝區',253:'石門區'}
dicnew={value:key for key, value in dcdict.items()}
distnum=[]
for x in range(len(h106ffff)):
    num=dicnew.get(h106ffff.iloc[x,1]) 
    distnum.append(num)
h106ffff['code']=distnum
# 交易年與建築完成年調整型態與格式並新增屋齡欄位
h106ffff['trade_year']=(h106ffff['交易年月日'].apply(lambda x: x[0:3])).astype(np.int64)
h106ffff['trade_month']=(h106ffff['交易年月日'].apply(lambda x: x[3:5])).astype(np.int64)
h106ffff['buildfinyear']=(h106ffff['建築完成年月'].apply(lambda x: x[0:3])).astype(np.int64)
h106ffff["houseage"]=h106ffff["trade_year"]-h106ffff["buildfinyear"]
# 建物型態編碼
bdstyle={"公寓(5樓含以下無電梯)":1,'華廈(10層含以下有電梯)':2,'住宅大樓(11層含以上有電梯)':3,
         '辦公商業大樓':4,'套房(1房1廳1衛)':5,'透天厝':6,'店面(店鋪)':7}
bsnum=[]
for x in range(len(h106ffff)):
    num=bdstyle.get(h106ffff.iloc[x,4]) 
    bsnum.append(num)
h106ffff['buildstyle']=bsnum
hm106=h106ffff.drop(columns=['鄉鎮市區', '主要用途',"建物型態","建物棟數","交易年月日",'建築完成年月'])
# 建物面積,單價元,總價轉換型態,並將管理組織改為數值
hm106['area']=hm106['建物移轉總面積平方公尺'].astype('float64')
hm106['pricettl']=hm106['總價元'].astype('int64')
hm106['priceper']=hm106['單價元平方公尺'].astype('float64')
hm106['rooms']=hm106['建物現況格局-房'].astype("int64")
hm106['manage_y1n0']=hm106['有無管理組織'].replace(to_replace="有", value=1,regex=True)
hm106['manage_y1n0']=hm106['manage_y1n0'].replace(to_replace="無", value=0,regex=True)

hm106=hm106.drop(columns=['交易標的', '土地區段位置建物區段門牌',"建物移轉總面積平方公尺",
                          "建物現況格局-房","有無管理組織",'總價元','單價元平方公尺','備註'])
hm106.to_csv(r'/Users/emilykuo/Documents/python project 2nd/dataset106h.csv')

# 預處理分類
datasets=pd.read_csv(r'/Users/emilykuo/Documents/python project 2nd/dataset106h.csv',
                     index_col=0)
datasets['classper']=(datasets['priceper']/10000).astype('int64')
for i in range(len(datasets)):
    if datasets.iloc[i,11]<=5:
        datasets.iloc[i,11]=1
    elif 5 < datasets.iloc[i,11]<=10:
        datasets.iloc[i,11]=2
    elif 10 < datasets.iloc[i,11]<=15:
        datasets.iloc[i,11]=3       
    elif 15 < datasets.iloc[i,11]<=20:
        datasets.iloc[i,11]=4        
    elif 20 < datasets.iloc[i,11]<=25:
        datasets.iloc[i,11]=5
    elif 25 < datasets.iloc[i,11]<=30:
        datasets.iloc[i,11]=6
    elif 30 < datasets.iloc[i,11]<=35:
        datasets.iloc[i,11]=7
    elif 35 < datasets.iloc[i,11]<=40:
        datasets.iloc[i,11]=8
    elif 40 < datasets.iloc[i,11]<=45:
        datasets.iloc[i,11]=9
    elif 45 < datasets.iloc[i,11]<=50:
        datasets.iloc[i,11]=10
    elif 50 < datasets.iloc[i,11]:
        datasets.iloc[i,11]=11

price=datasets.groupby('code').mean()

datasets.to_csv(r'/Users/emilykuo/Documents/python project 2nd/dataset106hclass.csv')

# ===================================================================================

h071=pd.read_csv(r'/Users/emilykuo/Desktop/實價登錄/F_lvr_land_A107S1.csv',index_col=1)
h072=pd.read_csv(r'/Users/emilykuo/Desktop/實價登錄/F_lvr_land_A107S2.csv',index_col=1)
h073=pd.read_csv(r'/Users/emilykuo/Desktop/實價登錄/F_lvr_land_A107S3.csv',index_col=1)
h074=pd.read_csv(r'/Users/emilykuo/Desktop/實價登錄/F_lvr_land_A107S4.csv',index_col=1)

h071.reset_index(drop=False, inplace=True) 
h071=h071.drop(index=0,axis=0)
h072.reset_index(drop=False, inplace=True) 
h072=h072.drop(index=0,axis=0)
h073.reset_index(drop=False, inplace=True) 
h073=h073.drop(index=0,axis=0)
h074.reset_index(drop=False, inplace=True) 
h074=h074.drop(index=0,axis=0)

hall07=pd.concat([h071,h072,h073,h074])
hall07.reset_index(drop=True, inplace=True)

import re
building=[]
for h in hall07['交易筆棟數'][:]:
    match = re.search('建物\d+', h)
    match = match.group()
    building.append(int(match[2:]))
hall07['建物棟數']=building
msk=hall07['建物棟數']!=0
h107f=hall07[msk]
mskuse=h107f['主要用途'] == '住家用'
h107ff=h107f[mskuse]

h107ff= h107ff.drop(columns=['土地移轉總面積平方公尺', '都市土地使用分區', '非都市土地使用分區',
                    '非都市土地使用編定','交易筆棟數', '移轉層次', '總樓層數', 
                    '主要建材','建物現況格局-廳', '建物現況格局-衛','建物現況格局-隔間',
                    '車位類別', '車位移轉總面積平方公尺', '車位總價元','編號'])

h107ff=h107ff.dropna(subset=['單價元平方公尺'])
h107ff["建築完成年月"]=h107ff["建築完成年月"].fillna("0500101")

mskb=h107ff['建物型態']!='其他'
h107fff=h107ff[mskb]
mskc=h107fff['建物型態']!='廠辦'
h107ffff=h107fff[mskc]

# use=h107ffff.groupby('建物型態')

# 行政區轉數字
dcdict={220:'板橋區',221:'汐止區',222:'深坑區',223:'石碇區',224:'瑞芳區',207:'萬里區',
208:'金山區',226:'平溪區',227:'雙溪區',228:'貢寮區',231:'新店區',232:'坪林區',233:'烏來區',234:'永和區',
235:'中和區',236:'土城區',237:'三峽區',238:'樹林區',239:'鶯歌區',241:'三重區',242:'新莊區',
243:'泰山區',244:'林口區',247:'蘆洲區',248:'五股區',249:'八里區',251:'淡水區',252:'三芝區',253:'石門區'}
dicnew={value:key for key, value in dcdict.items()}
distnum=[]
for x in range(len(h107ffff)):
    num=dicnew.get(h107ffff.iloc[x,1]) 
    distnum.append(num)
h107ffff['code']=distnum
# 交易年與建築完成年調整型態與格式並新增屋齡欄位
h107ffff['trade_year']=(h107ffff['交易年月日'].apply(lambda x: x[0:3])).astype(np.int64)
h107ffff['trade_month']=(h107ffff['交易年月日'].apply(lambda x: x[3:5])).astype(np.int64)
h107ffff['buildfinyear']=(h107ffff['建築完成年月'].apply(lambda x: x[0:3])).astype(np.int64)
h107ffff["houseage"]=h107ffff["trade_year"]-h107ffff["buildfinyear"]
# 建物型態編碼
bdstyle={"公寓(5樓含以下無電梯)":1,'華廈(10層含以下有電梯)':2,'住宅大樓(11層含以上有電梯)':3,
         '辦公商業大樓':4,'套房(1房1廳1衛)':5,'透天厝':6,'店面(店鋪)':7}
bsnum=[]
for x in range(len(h107ffff)):
    num=bdstyle.get(h107ffff.iloc[x,4]) 
    bsnum.append(num)
h107ffff['buildstyle']=bsnum
hm107=h107ffff.drop(columns=['鄉鎮市區', '主要用途',"建物型態","建物棟數","交易年月日",'建築完成年月'])
# 建物面積,單價元,總價轉換型態,並將管理組織改為數值
hm107['area']=hm107['建物移轉總面積平方公尺'].astype('float64')
hm107['pricettl']=hm107['總價元'].astype('int64')
hm107['priceper']=hm107['單價元平方公尺'].astype('float64')
hm107['rooms']=hm107['建物現況格局-房'].astype("int64")
hm107['manage_y1n0']=hm107['有無管理組織'].replace(to_replace="有", value=1,regex=True)
hm107['manage_y1n0']=hm107['manage_y1n0'].replace(to_replace="無", value=0,regex=True)

hm107=hm107.drop(columns=['交易標的', '土地區段位置建物區段門牌',"建物移轉總面積平方公尺",
                          "建物現況格局-房","有無管理組織",'總價元','單價元平方公尺','備註'])
hm107.to_csv(r'/Users/emilykuo/Documents/python project 2nd/dataset107h.csv')

datasets07=pd.read_csv(r'/Users/emilykuo/Documents/python project 2nd/dataset107h.csv',
                     index_col=0)

datasets07['classper']=(datasets07['priceper']/10000).astype('int64')
for i in range(len(datasets07)):
    if datasets07.iloc[i,11]<=5:
        datasets07.iloc[i,11]=1
    elif 5 < datasets07.iloc[i,11]<=10:
        datasets07.iloc[i,11]=2
    elif 10 < datasets07.iloc[i,11]<=15:
        datasets07.iloc[i,11]=3       
    elif 15 < datasets07.iloc[i,11]<=20:
        datasets07.iloc[i,11]=4        
    elif 20 < datasets07.iloc[i,11]<=25:
        datasets07.iloc[i,11]=5
    elif 25 < datasets07.iloc[i,11]<=30:
        datasets07.iloc[i,11]=6
    elif 30 < datasets07.iloc[i,11]<=35:
        datasets07.iloc[i,11]=7
    elif 35 < datasets07.iloc[i,11]<=40:
        datasets07.iloc[i,11]=8
    elif 40 < datasets07.iloc[i,11]<=45:
        datasets07.iloc[i,11]=9
    elif 45 < datasets07.iloc[i,11]<=50:
        datasets07.iloc[i,11]=10
    elif 50 < datasets07.iloc[i,11]:
        datasets07.iloc[i,11]=11
        
datasets07.to_csv(r'/Users/emilykuo/Documents/python project 2nd/dataset107hclass.csv')
        
        