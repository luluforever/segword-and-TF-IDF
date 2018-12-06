# -*- coding: utf-8 -*-
#需要自己修改路径的几个地方有（3个）：
#seg_word/：分词结果路径，与seg_word.py中的分词结果保存路径一样
#/TF-IDF：tf-idf保存路径
#python3.6
"""
Author: qinlu
Date: 2018.12.1
"""
import os
#计算tf-idf的模块
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

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

def Tfidf(filelist):
    # 读取已分词好的文档，进行TF-IDF计算
    # param filelist: 文件名列表
    # return:
    #分词保存的路径，根据情况修改
    path = 'seg_word/'
    corpus = []  # 存取分词结果
    for ff in filelist:
        fname = path + ff
        f = open(fname, 'r+')
        content = f.read()
        f.close()
        corpus.append(content)
    vectorizer = CountVectorizer()
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))
    word = vectorizer.get_feature_names()  # 所有文本的关键字
    weight = tfidf.toarray()  # 对应的tfidf矩阵
    #tf-idf保存路径，根据情况修改
    sFilePath = '/TF-IDF'
    if not os.path.exists(sFilePath):
        os.mkdir(sFilePath)
    # 这里将每份文档词语的TF-IDF写入tfidffile文件夹中保存
    for i in range(len(weight)):
        file_name = filelist[i].replace('-seg.txt', '')
        f = open(sFilePath + '/' + file_name + '.txt', 'w+')
        for j in range(len(word)):
            if weight[i][j] > 0:
                f.write(word[j] + "    " + str(weight[i][j]) + "\n")
        f.close()

if __name__ == "__main__":
    #根据情况将seg_word/改为分词结果路径
    allfile1 = getFilelist('seg_word/')
    Tfidf(allfile1)