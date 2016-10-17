from .matcher import Matcher

class WordWeightMatcher(Matcher):

    def __init__(self, segLib="Taiba"):
        super().__init__(segLib)

        self.segTitles = []
        self.initialize()

    def initialize(self):
        self.TitlesSegmentation()
        self.train_word_weight()

    def TitlesSegmentation(self):
        """
        回傳 self.titles 斷詞後的 title 列表
        """
        self.segTitles = []
        for title in self.titles:
            self.segTitles.append(self.wordSegmentation(title))

    def train_word_weight(self):
        # 算法推導請見：http://www.52nlp.cn/forgetnlp4
        




    def _coprus_to_bow(self):


    def match(self, query, sort=False):
        """
        讀入使用者 query，若語料庫中存在相同的句子，便回傳該句子與標號
        """

        ratio  = -1
        target = ""
        target_idx = -1

        for index,title in enumerate(self.titles):

            newRatio = fuzz.ratio(query, title)
            if newRatio >= ratio:
                ratio  = newRatio
                target = title
                target_idx = index

        if sort:
            #TODO 斷詞後將句子重組，待確認有效性
            pass

        return target,index
