import logging
import os
import math

from collections import defaultdict

from gensim import corpora

# 引入斷詞與停用詞的配置
from Matcher.matcher import Matcher

class Evaluator(Matcher):
    """
    讀入一串推文串列，計算出當中可靠度最高的推文
    """
    def __init__(self,segLib="Taiba"):

        #FIXME 若「線上版本」受記憶體容量限制，需考慮更換為 jieba!
        super().__init__(segLib)
        self.responses = []
        self.segResponses = []

        self.filteredWords = set() # 必須濾除的回應

        self.counterDictionary = defaultdict(int) # 用於統計詞頻
        self.tokenDictionary = None # 用於分配詞 id，與建置詞袋

        # 中文停用詞與特殊符號加載
        self.loadStopWords(path="data/stopwords/chinese_sw.txt")
        self.loadStopWords(path="data/stopwords/specialMarks.txt")
        self.loadFilterdWord(path="data/stopwords/ptt_words.txt")

    def getBestResponse(self, responses):
        """
        從 self.responses 中挑選出可靠度最高的回應回傳
        """
        self.buildResponses(responses)
        self.segmentResponse()
        self.buildCounterDictionary()
        response,grade = self.evaluateByGrade()

        return response,grade

    def loadFilterdWord(self,path):
        with open(path, 'r', encoding='utf-8') as sw:
            for word in sw:
                self.filteredWords.add(word.strip('\n'))

    def buildResponses(self, responses):
        """
        將 json 格式中目前用不上的 user,vote 去除，只留下 Content
        """
        self.responses = []
        for response in responses:
            clean = True
            r = response["Content"]
            for word in self.filteredWords:
                if word in r:
                    clean = False
            if clean:
                self.responses.append(response["Content"])

    def segmentResponse(self):
        """
        對 self.responses 中所有的回應斷詞並去除中文停用詞，儲存於 self.segResponses
        """
        self.segResponses = []
        for response in self.responses:
            keywordResponse = [keyword for keyword in self.wordSegmentation(response)
                               if keyword not in self.stopwords]
            self.segResponses.append(keywordResponse)
        #logging.info("已完成回應斷詞")

    def buildCounterDictionary(self):
        """
        統計 self.segResponses 中每個詞出現的次數
        """
        for reply in self.segResponses:
            for word in reply:
                self.counterDictionary[word] += 1
        #logging.info("計數字典建置完成")

    def buildTokenDictionary(self):
        """
        為 self.segResponses 中的詞配置一個 id
        """
        self.tokenDictionary = corpora.Dictionary(self.segResponses)
        logging.info("詞袋字典建置完成，%s" % str(self.tokenDictionary))

    def evaluateByGrade(self):
        """
        依照每個詞出現的在該文件出現的情形，給予每個回覆一個分數
        若該回覆包含越多高詞頻的詞，其得分越高

        Return: (BestResponse,Grade)
            - BestResponse: 得分最高的回覆
            - Grade: 該回覆獲得的分數
        """
        grade = -1.
        bestResponse = ""

        for i in range(0, len(self.segResponses)):
            wordCount = len(self.segResponses[i])
            if wordCount == 0: # 該回覆全為停用詞，無意義
                continue

            cur_grade = 0.

            for word in self.segResponses[i]:
                cur_grade += self.counterDictionary[word]
                cur_grade = cur_grade / math.log(len(self.segResponses[i])+1, 2)

            if cur_grade > grade:
                grade = cur_grade
                bestResponse = self.responses[i]

        return (bestResponse,grade)

class ClusteringEvaluator(Evaluator):
    """
    基於聚類評比推文可靠度
    """
    pass
