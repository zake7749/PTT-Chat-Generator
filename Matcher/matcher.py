import jieba
import Taiba

class Matcher(object):

    """
    比對使用者輸入的句子與目標語料集，
    回傳語料集中最相似的一個句子。
    """

    def __init__(segLib="jieba"):
        self.titles = []
        self.useTaiba = False

    def jiebaCustomSetting(self):
        pass

    def TaibaCustomSetting(self):
        pass

    def loadTitles(self, path):

        with open(path,'r',encoding='utf-8') as data:
            self.titles = [line.strip('\n') for line in data]

    def match(self, query):
        """
        讀入使用者 query，若語料庫中存在相同的句子，便回傳該句子與標號
        """
        result = None
        for index, title in enumerate(self.titles):
            if title == query:
                return title,index

    def wordSegmentation(self, string):

        if useTaiba:
            return Taiba.cut(string,cut_all=True)
        else:
            return jieba.cut(string,cut_all=True)
