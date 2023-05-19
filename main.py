# encoding=utf-8

import joblib
import numpy as np
import pandas as pd
from gensim.models import Word2Vec

import emotionDict
from Segment import Seg
from myUtils import clearn_str, createFeatureName


# from jd_spider import spider,getProductInfo

def set_default(obj):
    if isinstance(obj, set):
        return list(obj)
    raise TypeError


def getWordVecs(wordslist, model_):
    vec = []
    for word in wordslist:
        word = word.replace('\n', '')
        try:
            vec.append(model_.wv[word])
        except KeyError:
            # print(word)
            continue
    return np.array(vec, dtype='float')


def predict(sentence):
    if not sentence:
        return 'false'
    wds = Seg()
    sentence = clearn_str(sentence)
    seg_list = wds.cut(sentence, cut_all=False)
    word_model = Word2Vec.load('./model/word2_200wei.m')
    # 获得词向量
    vecs = getWordVecs(seg_list, word_model)
    if len(vecs) > 0:
        vecs_array = sum(np.array(vecs)) / len(vecs)  # 获取一个只有一列数组
        vecs_array = vecs_array.reshape(1, 200)  # 更新列数
        # 添加列名
        vecs_array = pd.DataFrame(vecs_array, columns=list(createFeatureName()))
        # 获取模型
        # clf = joblib.load("./model/model3_RF.m")
        clf = joblib.load("./model/model3_SVM_200wei.m")
        # clf = joblib.load("./model/model3_LR.m")
        ans = clf.predict_proba(vecs_array)  # 预测的概率
        # print(ans)
        diff = abs(round(ans[0][0] - ans[0][1], 3))
        # print(diff)
        sentiment_result, sentiment_words, score = emotionDict.classify_(sentence)
        # 如果差距太小，则表明不准确，需要使用情感词典辅助
        if diff < 0.2:
            return sentiment_result, sentiment_words, round(ans[0][0], 3), round(ans[0][1], 3)

        if ans[0][0] > ans[0][1]:
            return '消极', sentiment_words, round(ans[0][0], 3), round(ans[0][1], 3)
        else:
            return '积极', sentiment_words, round(ans[0][0], 3), round(ans[0][1], 3)


if __name__ == '__main__':
    print("")
    # print(predict('物流很快，活动价格买的，很实惠。物品也不错，挺好的购物体验。'))

    # sen, sen_list, negAns, posAns = predict('物流很快，活动价格买的，很实惠。物品也不错，挺好的购物体验。')
    # obj = {
    #     'sen': sen,
    #     'sen_list': sen_list,
    #     'negAns': negAns,
    #     'posAns': posAns
    # }

    # product_url = 'https://item.jd.com/100015056401.html?bbtf=1'
    product_url = 'https://item.jd.com/100005465673.html'

    # url = 'https://api.m.jd.com/?appid=item-v3&functionId=pc_club_productPageComments&client=pc&clientVersion=1.0.0&t=1684468692049&loginType=3&uuid=122270672.1683459379064608177886.1683459379.1684465032.1684468079.3&productId=100015056401&score=0&sortType=5&page=1&pageSize=10&isShadowSku=0&rid=0&fold=1&bbtf=1&shield='
    # spider(product_url)

    # getProductInfo(product_url)
