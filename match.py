
from Matcher.fuzzyMatcher import FuzzyMatcher

def main():
    fuzzyMatch()

def fuzzyMatch():

    fuzzyMatcher = FuzzyMatcher(segLib="Taiba")
    fuzzyMatcher.loadTitles(path="data/Titles.txt")

    while True:
        query = input("隨便輸入點什麼吧: ")
        title,index = fuzzyMatcher.match(query)
        print("最相似的標題是「%s」" % title)
    #load a custom user dictionary.
    #fuzzyMatcher.TaibaCustomSetting(usr_dict="jieba_dictionary/ptt_dic.txt")

    #load stopwords
    #fuzzyMatcher.loadStopWords(path="data/stopwords/chinese_sw.txt")
    #fuzzyMatcher.loadStopWords(path="data/stopwords/ptt_words.txt")
    #fuzzyMatcher.loadStopWords(path="data/stopwords/specialMarks.txt")

if __name__ == '__main__':
    main()
