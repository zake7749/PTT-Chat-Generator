from .matcher import Matcher
from snownlp import SnowNLP

class bestMatchingMatcher(Matcher):

    """
    基於 bm25 算法取得最佳關聯短語
    """

    def __init__(self, segLib="Taiba", removeStopWords=False):
        super().__init__(segLib)
        self.cleanStopWords = removeStopWords
        if removeStopWords:
            self.loadStopWords("data/stopwords/chinese_sw.txt")
            self.loadStopWords("data/stopwords/specialMarks.txt")

    def initialize(self,ngram=1):

        assert len(self.titles) > 0, "請先載入短語表"
        self.TitlesSegmentation()
        for n in range(0,ngram):
            self.addNgram(n)
        # snownlp setting
        self.sn = SnowNLP(self.segTitles)

    def addNgram(self,n):
        """
        擴充 self.seg_titles 為 n-gram
        """
        idx = 0

        for seg_list in self.segTitles:
            ngram = self.generateNgram(n,self.titles[idx])
            seg_list = seg_list + ngram
            idx += 1

    def generateNgram(self,n,sentence):
        return [sentence[i:i+n] for i in range(0,len(sentence)-1)]


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
        #print("BM UPPER BOUND: %d" % best_grade)

        self.similarity = float(max)/best_grade * 100 #百分制

        return target,target_idx
