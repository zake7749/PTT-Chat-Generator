from .matcher import Matcher
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

class FuzzyMatcher(Matcher):

    """
    基於萊文斯坦距離比對短語相似度
    """

    def __init__(self, segLib="Taiba"):
        super().__init__(segLib)

    def joinTitles(self):
        self.segTitles = ["".join(title) for title in self.segTitles]
        
    def match(self, query, sort=False):
        """
        讀入使用者 query，若語料庫中存在類似的句子，便回傳該句子與標號

        Args:
            - query: 使用者欲查詢的語句
            - sort: 是否不考慮詞序
        """
        ratio  = 1
        target = ""
        target_idx = -1

        if sort:
            query = self.wordSegmentation(query)
            query = "".join(query)
            title_list = self.segTitles
        else:
            title_list = self.titles

        for index,title in enumerate(title_list):

            newRatio = fuzz.ratio(query, title)
            if newRatio >= ratio:
                ratio  = newRatio
                target = title
                target_idx = index
        self.similarity = ratio

        return target,target_idx
