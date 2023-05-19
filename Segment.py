# encoding=utf-8
import codecs

import jieba  # 中文分词库
from myUtils import clearn_str

class Seg(object):
    stopword_filepath = "./stopwordList/stopword.txt"
    # stopword_filepath = "./data_dict/stopwords_dict.txt"

    def __init__(self):
        self.stopwords = set()
        self.read_in_stopword()


    def read_in_stopword(self):
        file = codecs.open(self.stopword_filepath, 'r', 'utf-8')
        while True:
            line = file.readline()
            line = line.strip('\r\n')
            if not line:
                break
            self.stopwords.add(line)
        file.close()

    def cut(self, sentence, cut_all=False):
        sentence = clearn_str(sentence)
        seg_list = jieba.cut(sentence, cut_all)
        results = []
        for seg in seg_list:
            if seg in self.stopwords:
                continue
            results.append(seg)
        return results

