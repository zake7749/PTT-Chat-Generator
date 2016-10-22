import json
import os
import random

from Matcher.fuzzyMatcher import FuzzyMatcher
from Matcher.wordWeightMatcher import WordWeightMatcher
from Matcher.matcher import Matcher

def main():
    matcherTesting("Fuzzy")

def getMatcher(matcherType,sort=False):

    """
    回傳初始完畢的 Matcher

    Args:
        - matcherType:要使用哪種字串匹配方式
            - Fuzzy
            - WordWeight
        - sort:
            - a boolean value for fuzzy sorting match.
    """

    if matcherType == "WordWeight":
        return woreWeightMatch()
    elif matcherType == "Fuzzy":
        return fuzzyMatch(sort)
    elif matcherType == "Vectorize":
        pass #TODO
    elif matcherType == "DeepLearning":
        pass #TODO
    else:
        print("[Error]: Invailded type.")
        exit()

def matcherTesting(matcherType, sort=False):

    matcher = getMatcher(matcherType,sort)
    while True:
        query = input("隨便說些什麼吧: ")
        title,index = matcher.match(query,sort)
        sim = matcher.getSimilarity()
        print("最為相似的標題是 %s ，相似度為 %d " % (title,sim))

        res = json.load(open(os.path.join("data/processed/reply/",str(int(index/1000))+'.json'),'r',encoding='utf-8'))
        targetId = index % 1000
        #randomId = random.randrange(0,len(res[targetId]))

        for content in res[targetId]:
            print(content["Content"])


def woreWeightMatch():

    weightMatcher = WordWeightMatcher(segLib="Taiba")
    weightMatcher.loadTitles(path="data/Titles.txt")
    weightMatcher.initialize()
    return weightMatcher

def fuzzyMatch(sort=False):
    fuzzyMatcher = FuzzyMatcher(segLib="Taiba")
    fuzzyMatcher.loadTitles(path="data/Titles.txt")
    if sort:
        fuzzyMatcher.TitlesSegmentation()
        fuzzyMatcher.joinTitles()
    return fuzzyMatcher

    #load a custom user dictionary.
    #fuzzyMatcher.TaibaCustomSetting(usr_dict="jieba_dictionary/ptt_dic.txt")

    #load stopwords
    #fuzzyMatcher.loadStopWords(path="data/stopwords/chinese_sw.txt")
    #fuzzyMatcher.loadStopWords(path="data/stopwords/ptt_words.txt")
    #fuzzyMatcher.loadStopWords(path="data/stopwords/specialMarks.txt")


if __name__ == '__main__':
    main()
