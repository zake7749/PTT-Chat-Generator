from .matcher import Matcher
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

class FuzzyMatcher(Matcher):

    """
    基於萊文斯坦距離比對短語相似度
    """

    def __init__(self, segLib="Taiba"):
        super().__init__(segLib)

    def match(self, query, sort=False):
        """
        讀入使用者 query，若語料庫中存在相同的句子，便回傳該句子與標號
        """

        ratio  = 1
        target = ""
        target_idx = -1

        #target,ratio = process.extractOne(query, self.titles)

        for index,title in enumerate(self.titles):

            newRatio = fuzz.ratio(query, title)
            if newRatio >= ratio:
                ratio  = newRatio
                target = title
                target_idx = index

        self.similarity = ratio

        if sort:
            #TODO 斷詞後將句子重組，待確認有效性
            pass

        return target,target_idx
