
from Matcher.fuzzyMatcher import FuzzyMatcher

def main():
    fuzzyMatch(threshold=50)

def fuzzyMatch(threshold):

    fuzzyMatcher = FuzzyMatcher(segLib="Taiba")
    fuzzyMatcher.loadTitles(path="data/Titles.txt")

    while True:
        query = input("隨便輸入點什麼吧: ")
        title,index = fuzzyMatcher.match(query)
        sim = fuzzyMatcher.getSimilarity()
        if threshold < sim:
            print("最相似的標題是「%s」，相似度高達 %d" % (title,sim))
        else:
            print("在閥值為 %d 的情況下，找不到足夠相似的標題 :<" % threshold)
            print("目前最佳解為「%s」，相似度只有 %d" % (title,sim))
    #load a custom user dictionary.
    #fuzzyMatcher.TaibaCustomSetting(usr_dict="jieba_dictionary/ptt_dic.txt")

    #load stopwords
    #fuzzyMatcher.loadStopWords(path="data/stopwords/chinese_sw.txt")
    #fuzzyMatcher.loadStopWords(path="data/stopwords/ptt_words.txt")
    #fuzzyMatcher.loadStopWords(path="data/stopwords/specialMarks.txt")


if __name__ == '__main__':
    main()
