from collections import defaultdict

import jieba
import pandas as pd

from myUtils import clearn_str


def seg_word(sentence):
    if isinstance(sentence, list):
        sentence = ''.join(sentence)

    sentence = clearn_str(sentence)
    # 得到分词数据
    seg_list = jieba.cut(sentence)
    seg_result = []

    # 生成停用词表
    stopwords = set()
    with open('data_dict/stopwords_dict.txt', 'r', encoding='utf-8') as f:
        for i in f:
            stopwords.add(i.strip())
    f.close()

    # 去停用词
    for i in seg_list:
        if i in stopwords:
            pass
        else:
            seg_result.append(i)

    return seg_result


def classify_(sentence):
    # 获取分词后的数据
    wordlist = seg_word(sentence)

    if len(wordlist) == 0:
        return 0

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

    # 构建符号列表
    symbol_list = ['?', '!', '？', '！']

    sen_words = set()  # 存储修正词
    wordsinPosNeg = set()  # 存储积极或者消极词
    not_list = []  # 存储否定词系数
    deg_list = []  # 存储程度系数
    score = 0  # 分数结果

    for i in wordlist:
        # print(i)
        if i in sen_dict.keys() and i not in posWords_list and i not in negWords_list:
            # 如果在情感词典中，但既不是正面词也不是负面词，为了修正
            sen_words.add(i)
        # if i in posWords_list or i in negWords_list or i in notWords_list:
        if i in posWords_list or i in negWords_list:
            # 如果是关键情感词，保存起来
            wordsinPosNeg.add(i)
        if i in sen_dict.keys() and i not in notWords_list and i not in degree_dict.keys():
            # 如果已经存储有程度系数或者否定系数，就拿出计算，如果没有就赋值1
            if len(deg_list) == 0:
                deg_list.append(1)

            if len(not_list) == 0:
                not_list.append(1)

            # 计算得分
            score += float(sen_dict[i]) * float(deg_list.pop(0)) * float(not_list.pop(0))
            # print(score)
        elif i in notWords_list:
            # 如果是否定词
            if len(not_list) != 0:
                not_list[0] *= -1
            else:
                not_list.append(-1)

        elif i in degree_dict.keys():
            # 如果是程度词
            if len(deg_list) != 0:
                deg_list[0] *= degree_dict[i]
            else:
                deg_list.append(degree_dict[i])
        elif i in symbol_list:
            score *= 1.2

    while score > 100000:
        score = score / 2

    score = round(score, 3)

    # 对情感词典中无关词进行评分修正
    for i in sen_words:
        if float(sen_dict[i]) < 0 <= score:
            sen_dict[i] += 0.01
        if float(sen_dict[i]) > 0 >= score:
            sen_dict[i] -= 0.01

    # 将修正后的结果重新写入情感词典文件
    # target = open('./data_dict/BosonNLP_sentiment_score.txt', 'w', encoding='utf-8')
    # for key, value in sen_dict.items():
    #     target.writelines(str(key) + ' ' + str(value) + '\n')
    # target.close()
    # print(f"本次修正的词汇为：{' '.join(sen_words)}")

    if len(wordsinPosNeg) == 0:
        wordsinPosNeg.add('null')

    if score > 0:
        return "积极", wordsinPosNeg, score
    else:
        return "消极", wordsinPosNeg, score
