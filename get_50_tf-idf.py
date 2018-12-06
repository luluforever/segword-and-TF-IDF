# -*- coding: utf-8 -*-
#需要自己修改路径的几个地方有（4个）：
#/TF-IDF：tf-idf的保存路径
#/TF-IDF1：tf-idf前50的保存路径
#python3.6
"""
Author: qinlu
Date: 2018.12.1
"""

import os
import pandas as pd

def getFilelist(a):
    #读取文件夹中的文件名
    #param a: 文件夹路径
    #return: filelist为list类型
    path = a
    filelist = []
    files = os.listdir(path)
    for f in files:
        filelist.append(f)
    return filelist
#/TF-IDF:tf-idf保存路径
allfile = getFilelist('/TF-IDF')
#/TF-IDF1:tf-idf前50的保存路径
allfile1 = getFilelist('/TF-IDF1')
os.chdir('/TF-IDF')
path = '/TF-IDF1'
j = 0
#获取每篇文章中tf-idf前50的词并保存在’/TF-IDF1’路径下
for i in allfile:
    if i not in allfile1:
        try:
            a=pd.read_csv(i,sep='    ',header=None,engine='python')
            a1=a[a[1]>0]
            a1=a1.sort_values(by = [1],axis = 0,ascending = False)
            if len(a1) <=50:
                filename=i.replace('.txt','')
                path1 = path+'/'+filename+'.txt'
                a1.to_csv(path1,sep='\t',header=None,index=False)
            else:
                a2 = a1.iloc[0:50,:]
                filename=i.replace('.txt','')
                path1 = path+'/'+filename+'.txt'
                a2.to_csv(path1,sep='\t',header=None,index=False)
        except Exception as e:
            #print(i)
            j = j+1
print('执行完毕！')