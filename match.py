
from Matcher.fuzzyMatcher import FuzzyMatcher
from Matcher.wordWeightMatcher import WordWeightMatcher
from Matcher.matcher import Matcher

def main():
    fuzzyMatch(threshold=50)
    #woreWeightMatch(threshold=0.5)


def getMatcher(matcherType):

    if matcherType == "WordWeight":
        return woreWeightMatch()
    elif matcherType == "Fuzzy":
        return fuzzyMatch()
    elif matcherType == "Vectorize":
        pass #TODO
    elif matcherType == "DeepLearning":
        pass #TODO
    else:
        print("[Error]: Invailded type.")
        exit()

def woreWeightMatch(threshold):

    weightMatcher = WordWeightMatcher(segLib="Taiba")
    weightMatcher.loadTitles(path="data/Titles.txt")
    weightMatcher.initialize()
    return weightMatcher

def fuzzyMatch(threshold):
    fuzzyMatcher = FuzzyMatcher(segLib="Taiba")
    fuzzyMatcher.loadTitles(path="data/Titles.txt")
    return fuzzyMatcher

    #load a custom user dictionary.
    #fuzzyMatcher.TaibaCustomSetting(usr_dict="jieba_dictionary/ptt_dic.txt")

    #load stopwords
    #fuzzyMatcher.loadStopWords(path="data/stopwords/chinese_sw.txt")
    #fuzzyMatcher.loadStopWords(path="data/stopwords/ptt_words.txt")
    #fuzzyMatcher.loadStopWords(path="data/stopwords/specialMarks.txt")


if __name__ == '__main__':
    main()
