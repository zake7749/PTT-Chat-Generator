import json
import os

def main():

    Filter = ArticleFilter()
    #reader.process_raw_data("data/raw/",is_dir=True)
    Filter.load_processed_corpus()
    Filter.process_raw_data("data/raw/",is_dir=True,to_one_file=True)

    Filter.print_titles()
    # Filter.print_user_info() TODO?

class ArticleFilter(object):

    def __init__(self):

        self.stopwords = None
        self.stoptags = None
        self.raw_data = None
        self.corpus = None

        self.titles = set()
        self.users_info = {}
        self.init_load_stopwords()

    def init_load_stopwords(self):

        """
        回應過濾用語集，如5樓、幫補血、紅明顯等不適用於聊天機器人的回應
        """
        with open('data/stopwords/ptt_words.txt','r', encoding='utf-8') as sw:
            self.stopwords = [word.strip('\n') for word in sw]
        with open('data/stopwords/gossiping.tag','r', encoding='utf-8') as sw:
            self.stoptags = [word.strip('\n') for word in sw]

    def process_raw_data(self, path, is_dir=False, to_one_file=False, one_file_name="corpus.json"):

        data = []
        total = []
        filename = None

        if is_dir:
            filenames = [name for name in os.listdir(path)]
        else:
            filenames = [path]

        for filename in filenames:
            with open(os.path.join(path, filename),'r', encoding="utf-8") as data:

                res = self.generate_corpus(json.load(data))

                if to_one_file:
                    total += res
                else:
                    with open("data/processed/"+filename,'w', encoding='utf-8') as op:
                        op.write(json.dumps(res, indent=4, ensure_ascii=False))
                        print("已處理 " + filename)
        if to_one_file:
            with open("data/processed/" + one_file_name,'w', encoding='utf-8') as op:
                op.write(json.dumps(total, indent=4, ensure_ascii=False))

    def merge_coprus(self, path="data/processed/"):

        corpus_names = [name for name in os.listdir(path)]
        all_corpus = []
        for corpus_name in corpus_names:
            with open(os.path.join(path, corpus_name),'r', encoding='utf-8') as data:
                c = json.load(data)
                all_corpus += c
        with open("data/processed/all_corpus.json", 'w', encoding='utf-8') as op:
            op.write(json.dumps(all_corpus, indent=4, ensure_ascii=False))

    def load_processed_corpus(self, path="data/processed/"):

        corpus_names = [name for name in os.listdir(path)]

        if len(corpus_names) != 0:
            for corpus_name in corpus_names:
                with open(os.path.join(path, corpus_name),'r', encoding='utf-8') as data:
                    c = json.load(data)
                    self.corpus += c

            for article in self.corpus:
                self.titles.add(article["Title"])


    def generate_corpus(self, articles, drop_response=True, negative_tag=None, no_content=True):

        """
        依據需求挑選出符合語料庫需求的文章

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
                print("NO DATA" + str(article))
                continue

            if title in self.titles:
                #捨去標題重複的文章
                continue

            if "Responses" in article.keys():
                article["Responses"] = self.clean_responses(article["Responses"])
                if no_content:
                    article.pop("Content")

            if drop_response:
                #捨去回應類文章與快訊文章
                if title.startswith("Re") or title.startswith("Fw"):
                    continue

            tag, title = self.get_tag(title)
            if tag in negative_tag:
                continue

            article["Tag"]   = tag
            article["Title"] = title
            self.titles.add(title)

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

            self._update_users_history(response) # 更新使用者推噓文紀錄

            # 濾除過短與特定使用者的回應
            if response["User"] in negative_user or len(response["Content"]) < min_length:
                continue
            for w in stopwords:
                if w in response["Content"]: # 濾除包含停用詞的回應
                    continue

            clean_responses.append(response)

        return clean_responses

    def _update_users_history(self, response):

        """
        記錄 user 的推/噓/箭頭
        """

        user = response["User"]

        if user not in self.users_info.keys():

            res = {
                "推":0,
                "噓":0,
                "箭頭":0
            }
            self.users_info[user] = res

        if response["Vote"] == "推":
            self.users_info[user]["推"] += 1
        elif response["Vote"] == "噓":
            self.users_info[user]["噓"] += 1
        else:
            self.users_info[user]["箭頭"] += 1


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

    def print_user_info(self):
        with open('data/User_info.txt','w',encoding='utf-8') as op:
            op.write(json.dumps(self.users_info, indent=4, ensure_ascii=False))


class User(object):
    pass

class QAPair(object):

    def __init__():

        self.tag      = ""
        self.title    = ""
        self.author   = ""
        self.response = None

if __name__ == '__main__':
    main()
