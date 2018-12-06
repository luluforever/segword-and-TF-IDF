# -*- coding: utf-8 -*-
#需要自己修改路径的几个地方有（5个）：
#workspace/：工作目录
#stop_word.txt：停用词典路径
#article_data1.csv：文章路径
#seg_word/：分词结果保存路径
#yxdict2.txt：医学词典路径

#python3.6
"""
Author: qinlu
Date: 2018.12.1
"""
import os
import re
#导入结巴分词模块
import jieba
import jieba.posseg as pseg
#导入多线程模型
import threading
import sys
import string
import time
import pandas as pd

#设置工作目录，将'workspace/'设置为自己的工作目录路径
os.chdir('workspace/')

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


def creatstoplist(stopwordspath):
    # 创建停用词列表
    #param stopwordspath: 停用词表路径
    #return: stwlist为list类型
    f = open(stopwordspath, 'r', encoding='utf-8')
    lines = f.readlines()  # 读取全部内容
    stwlist = []
    for line in lines:
        #去掉换行符
        line1 = line.strip('\n')
        stwlist.append(str(line1))
    return set(stwlist)



def fenci(title,text, stwList):
    # 对文档进行分词处理udan，只提取出名词
    #param title: 文章id
    #param text: 文章内容
    #param stwList: 停用词列表
    #return:
    text = text.encode('utf-8')
    text = text.decode('utf-8')
    # 保存分词结果的目录，根据自己情况换为自己的分词结果保存路径
    sFilePath = 'seg_word/'
    if not os.path.exists(sFilePath):
        os.mkdir(sFilePath)
    # 对文档进行分词处理,采用精确模式,同时加载医学词典，换为自己的医学词典路径
    jieba.load_userdict("yxdict.txt")
    seg_list = pseg.cut(text)

    # 对空格，换行符,数字，停用词进行处理
    result = []
    for seg1 in seg_list:
        #去除空格
        seg = ''.join(seg1.word.split())
        #去除头尾空格
        seg = seg.strip()
        if (seg != '' and seg != "\n" and seg != "\n\n"):
            #判断是否在停用词表中
            if seg not in stwList:
                #判断词的长度是否大于1，以及是否全部由数字组成
                if (len(seg) > 1 and seg != '\t' and seg.isdigit() == False):
                    #判断是否是名词
                    if seg1.flag in ['n','nr','ns','nt','nz']:
                        result.append(seg)
    # 将分词后的结果用空格隔开，保存至本地。比如"我来到上海医生站总部"，分词结果写入为："我 来到 上海 医生站 总部"
    f = open(sFilePath +str(title) + "-seg.txt", "w+")
    f.write(' '.join(result))
    f.close()

def thread_fenci(i):
    #批量分词，每次分词10000个文章
    start = 10000*(i)
    end = 10000*(i+1)
    #生成停用词表，记得对应修改路径
    stwlist = creatstoplist("stop_word.txt")
    #读取文章
    article = pd.read_csv('article_data1.csv')
    article1 = article.iloc[start:end,:]
    titles = article1['art_id']
    texts = article1['content']
    for num in range(start,end):
        fenci(titles[num],texts[num], stwlist,num)
if __name__ == "__main__":
    #采用多线程的方法运行程序
    thread = []
    for i in range(0,11):
        t = threading.Thread(target = thread_fenci,args = (i,))
        thread.append(t)
        t.start()
    for t in thread:
        t.join
    print('执行完毕')

