from .matcher import Matcher
from snownlp import SnowNLP

class bestMatchingMatcher(Matcher):

    """
    基於萊文斯坦距離比對短語相似度
    """

    def __init__(self, segLib="Taiba", removeStopWords=False):
        super().__init__(segLib)
        self.cleanStopWords = removeStopWords
        if removeStopWords:
            self.loadStopWords("data/stopwords/chinese_sw.txt")
            self.loadStopWords("data/stopwords/specialMarks.txt")

        self.TitlesSegmentation()
        # snownlp setting
        self.sn = SnowNLP(self.segTitles)

    def joinTitles(self):
        self.segTitles = ["".join(title) for title in self.segTitles]

    def match(self, query):
        """
        讀入使用者 query，若語料庫中存在類似的句子，便回傳該句子與標號

        Args:
            - query: 使用者欲查詢的語句
        """

        #FIXME STILL ABLE TO OPTIMIZE. 可以整體化

        seg_query = self.wordSegmentation(query)
        res = self.sn.sim(seg_query)

        max = -999.0
        target_idx = 0
        idx = 0

        for score in res:
            if score > max:
                max = score
                target_idx = idx
                target = "".join(self.segTitles[target_idx])
            idx += 1

        #FIXME NEED OPTIMIZE
        best_grade = self.sn.sim(self.segTitles[target_idx])[target_idx]
        print("BM UPPER BOUND: %d" % best_grade)

        self.similarity = float(max)/best_grade * 100 #百分制

        return target,target_idx
