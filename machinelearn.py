#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 17:44:09 2020

@author: emilykuo
"""
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import cluster, neighbors, tree

datasets=pd.read_csv(r'/Users/emilykuo/Documents/python project 2nd/dataset106hclass.csv',
                     index_col=0)
# Knn ===========================================================

knnx=datasets.drop(columns=['priceper','pricettl','trade_month','classper'])
knny=datasets['classper']

# 測試Ｋ值
# for i in range(1,100,1):
#     knn=neighbors.KNeighborsClassifier(n_neighbors=i)
#     knn.fit(knnx,knny)
#     print("分類-驗證KNN準確率:",i, knn.score(knntestx,knntesty))
# 選擇k=5

knn=neighbors.KNeighborsClassifier(n_neighbors=5)
knn.fit(knnx,knny)
predy=knn.predict(knnx)

print("分類-KNN準確率106年:",knn.score(knnx,knny))

# 驗證在107年資料
datasets07=pd.read_csv(r'/Users/emilykuo/Documents/python project 2nd/dataset107hclass.csv',
                     index_col=0)
knntestx=datasets07.drop(columns=['priceper','pricettl','trade_month','classper'])
knntesty=datasets07['classper']
predy07=knn.predict(knntestx)
print("分類-驗證KNN準確率107年:",knn.score(knntestx,knntesty))



# tree ===========================================================

treex=datasets.drop(columns=['priceper','pricettl','trade_month','classper'])
treey=datasets['classper']
treetestx07=datasets07.drop(columns=['priceper','pricettl','trade_month','classper'])
treetesty07=datasets07['classper']
dtree= tree.DecisionTreeClassifier(max_depth=8)
clf=dtree.fit(treex, treey)

print("準確率:", dtree.score(treex, treey))
print("準確率:", dtree.score(treetestx07, treetesty07))
font={'family':'PingFang HK','weight':'bold', 'size':'10'}
plt.rc('font',**font)
plt.rc('axes',unicode_minus=False)
plt.rcParams['figure.dpi'] = 500


plt.figure(figsize=(6,3))
tree.plot_tree(clf, filled=True)
plt.title("Decision trees")
plt.show()




