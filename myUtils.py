# -*- coding:utf-8 -*-
from __future__ import print_function

import re
from collections import Counter, defaultdict

import matplotlib.pyplot as plt
import pandas as pd
from wordcloud import WordCloud


def createFeatureName():
    res = ['0.1']
    for i in range(1, 200):
        res.append(str(i))
    return res


# 通过正则表达式筛除string中的标点符号，数字
def clearn_str(string):
    # 筛除掉中文标点
    string = re.sub(r'[＂＃＄％＆＇（）＊＋，－／：；＜$￥＝＞＠［'
                    r'＼］＾＿｀｛｜｝～｟｠｢｣､　、〃〈〉《》「」'
                    r'『』【】〔〕〖〗〘〙〚〛〜〝〞〟〰〾〿–—‘’'
                    r'‛“”„‟…‧﹏﹑﹔·｡。 ]', '', string)
    # 筛除掉英文标点
    string = re.sub(r"[\"#$%&'()*+,-./:;<=>@^_`{|}~]", '', string)
    # 删除数字，字母
    string = re.sub(r'[a-zA-Z0-9]', '', string)
    return string


def getTheChiPin():
    # with open('./test_data/pintuSeg.txt', 'r', encoding='utf-8') as f:
    #     lines = f.readlines()

    # 中文分词
    words = []  # 每一项是一个词

    # for line in lines:
    #     words.extend(line.strip().split(' '))

    # # 统计词频
    word_counts = Counter(words)
    top_words = dict(word_counts.most_common(20))  # 获取前10个出现频率最高的单词
    #
    # # 生成柱状图
    plt.bar(top_words.keys(), top_words.values())
    plt.title('Top 20 Words')
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45, ha='right')

    plt.show()
    # # 保存图像
    plt.savefig('./static/img/chipinoutput.png')


def getTheWordCloud():
    with open('./test_data/pintuSeg.txt', 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # 中文分词
    words = []

    for line in lines:
        words.extend(line.strip().split(' '))
    # mask = np.array(Image.open('shape.png'))
    wc = WordCloud(font_path='simhei.ttf', background_color='black')

    # 统计词频并生成词云图
    word_cloud = wc.generate(' '.join(words))

    # 显示词云图
    plt.imshow(word_cloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()


def getSentimentWords(myList):
    # 构建情感词典
    file = open('data_dict/BosonNLP_sentiment_score.txt', 'r', encoding='utf-8')
    line = file.readlines()
    sen_dict = defaultdict()
    for i in line:
        arr = i.split(' ')
        if len(arr) == 2:
            sen_dict[arr[0]] = round(float(arr[1].strip()), 10)
    file.close()

    # 构建否定词列表
    notWords_file = open('data_dict/否定词.txt', 'r', encoding='utf-8')
    notWords_list = [w.strip() for w in notWords_file.readlines()]
    notWords_file.close()

    # 构建正面情绪词
    posWords_file = open('data_dict/正面情绪词.txt', 'r', encoding='utf-8')
    posWords_list = [w.strip() for w in posWords_file.readlines()]
    posWords_file.close()

    # 构建负面情绪词
    negWords_file = open('data_dict/负面情绪词.txt', 'r', encoding='utf-8')
    negWords_list = [w.strip() for w in negWords_file.readlines()]
    negWords_file.close()

    # 构建程度词字典
    degree_file = open('data_dict/程度副词.txt', 'r', encoding='utf-8')
    degree_list = degree_file.readlines()
    degree_dict = defaultdict()
    for i in degree_list:
        arr = i.split(',')
        degree_dict[arr[0]] = float(arr[1].strip())
    degree_file.close()

    resultList = []

    for w in myList:
        if w in sen_dict.keys() or w in notWords_list or w in posWords_list or w in negWords_list or w in degree_list:
            resultList.append(w)

    return resultList


def getSomeTestData():
    df = pd.read_csv('./data/data2.csv')
    df1 = df[(df['cat'] == '水果') & (df['label'] == 1)]
    df1 = df1.sample(n=500, axis=0)
    df1 = df1[['review']]
    df1.to_csv('./test_data/水果_1.csv', encoding='utf-8', index=False)

    df0 = df[(df['cat'] == '水果') & (df['label'] == 0)]
    df0 = df0.sample(n=500, axis=0)
    df0 = df0[['review']]
    df0.to_csv('./test_data/水果_0.csv', encoding='utf-8', index=False)
