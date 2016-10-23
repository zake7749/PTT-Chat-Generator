from responsesEvaluate import Evaluator

import match
import json
import os
import logging

def main():

    chatter = GossipBot()
    chatter.chatTime()

class GossipBot(object):

    """
    八卦板聊天機器人 ob'_'ov
    """
    def __init__(self):
        self.matcher = match.getMatcher("Fuzzy")
        self.evaluator = Evaluator()
        self.testSegment()
        logging.basicConfig(level=logging.WARNING) #若發生錯誤需要 DEBUG 請更改為 INFO


    def testSegment(self):
        logging.info("測試斷詞模塊中")
        try:
            self.matcher.wordSegmentation("測試一下斷詞")
            logging.info("測試成功")
        except Exception as e:
            logging.info(repr(e))
            logging.info("模塊載入失敗，請確認data與字典齊全")

    def chatTime(self):
        print("Bot: 你好啊，旅行者，讓我們來聊聊八卦吧 o_o ")
        while True:
            query = input()
            print("Bot: " +self.getResponse(query))

    def getResponse(self,query,threshold=30):

        title,index = self.matcher.match(query)
        sim = self.matcher.getSimilarity()
        if sim < threshold:
            return "你在說什麼呢"
        else:
            res = json.load(open(os.path.join("data/processed/reply/",str(int(index/1000))+'.json'),'r',encoding='utf-8'))
            targetId = index % 1000
            reply,grade = self.evaluator.getBestResponse(res[targetId])
            return reply

if __name__=="__main__":
    main()
