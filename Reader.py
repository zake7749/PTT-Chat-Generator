import json
import os


def main():

    reader = Reader()
    reader.process_raw_data("data/raw/",is_dir=True)
    reader.print_titles()

class Reader(object):

    def __init__(self):

        self.stopwords = None
        self.stoptags = None
        self.titles = []
        self.init_load_stopwords()

    def init_load_stopwords(self):

        """
        回應過濾用語集，如5樓、幫補血、紅明顯等不適用於聊天機器人的回應
        """
        with open('data/stopwords/ptt_words.txt','r', encoding='utf-8') as sw:
            self.stopwords = [word.strip('\n') for word in sw]
        with open('data/stopwords/gossiping.tag','r', encoding='utf-8') as sw:
            self.stoptags = [word.strip('\n') for word in sw]

    def process_raw_data(self, path, is_dir=False):

        data = []
        filename = None

        if is_dir:
            filenames = [name for name in os.listdir(path)]
        else:
            filenames = [path]

        for filename in filenames:
            with open(os.path.join(path, filename),'r', encoding="utf-8") as data:
                res = self.select_articles(json.load(data))
                f = open("data/processed/"+filename,'w', encoding='utf-8')
                f.write(json.dumps(res, indent=4, ensure_ascii=False))
                print("已處理 " + filename)
                f.close()

    def select_articles(self, articles, drop_response=True, negative_tag=None, no_content=True):

        """
        依據需求挑選出需要的文章

        Args:
            - articles: 描述文章的字典，格式參見 PTT-Crawler
            - drop_response: 是否濾除回應文章
            - negative_tag: 要濾除的標籤集
            - no_content: 是否需要保存文章內容
        """

        if negative_tag is None:
            negative_tag = self.stoptags

        clean_article = []

        for article in articles:

            try:
                #TODO 有些空頁面會造成錯誤 (atricle = {})
                title = article["Title"]
            except:
                print(str(article))
                continue

            if drop_response:
                if title.startswith("Re") or title.startswith("Fw"):
                    continue

            tag, title = self.get_tag(title)
            if tag in negative_tag:
                continue

            article["Tag"]   = tag
            article["Title"] = title
            self.titles.append(title)

            if "Responses" in article.keys():
                article["Responses"] = self.clean_responses(article["Responses"])
                if no_content:
                    article.pop("Content")

            clean_article.append(article)

        return clean_article

    def clean_responses(self, responses, negative_user=set(), min_length=3, stopwords=None):

        """
        濾除不需要的回應

        Args:
            responses: 回應的 dictionary
            negative_user: 要濾除該 User set 的回應
            min_length: 濾除低於 min_length 的回應
            stopwords: 濾除有敏感字詞的回應
        """

        if stopwords is None:
            stopwords = self.stopwords

        clean_responses = []

        for response in responses:
            if response["User"] in negative_user or len(response["Content"]) < min_length:
                continue
            for w in stopwords:
                if w in response["Content"]:
                    continue
            clean_responses.append(response)

        return clean_responses

    def get_tag(self, title):

        """
        回傳文章標籤與清理好的標題
        """

        try:
            tag,title = title.split("]",1)
        except:
            #print("發現無標籤標題: " + title)
            return None,title

        title = title.lstrip()
        return tag[1:],title

    def print_titles(self):
        with open('data/Titles.txt','w',encoding='utf-8') as op:
            for title in self.titles:
                op.write(title + "\n")


class QAPair(object):

    def __init__():

        self.tag      = ""
        self.title    = ""
        self.author   = ""
        self.response = None

if __name__ == '__main__':
    main()
