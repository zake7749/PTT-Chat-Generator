from . import Matcher
from fuzzywuzzy import fuzz

class FuzzyMatcher(Matcher):

    def match(self, query, sort=False):
        """
        讀入使用者 query，若語料庫中存在相同的句子，便回傳該句子與標號
        """

        ratio  = -1
        target = ""

        for title in self.titles:

            newRatio = fuzz.ratio(query, title)
            if newRatio >= ratio:
                ratio  = newRatio
                target = title

        if sort:
            #TODO 斷詞後以空白將句子重組
            pass

        return target
