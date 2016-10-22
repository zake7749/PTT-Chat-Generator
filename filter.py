import json
import logging
import os

def main():

    Filter = ArticleFilter()
    #Filter.load_processed_corpus()
    Filter.process_raw_data("data/raw/",is_dir=True,to_one_file=True)

    Filter.print_titles()
    Filter.print_response()
    # Filter.print_user_info() TODO?

class ArticleFilter(object):

    def __init__(self):

        self.stopwords = None
        self.stoptags = None
        self.raw_data = None
        self.corpus = []
        self.order_response = []
        self.order_titles = []

        self.article_count = 0

        self.titles = set()
        self.users_info = {}

        self.init_load_stopwords()

        logging.basicConfig(format='%(asctime)s : %(threadName)s : %(levelname)s : %(message)s', level=logging.INFO)

    def init_load_stopwords(self):

        """
        回應過濾用語集，如5樓、幫補血、紅明顯等不適用於聊天機器人的回應
        """
        with open('data/stopwords/ptt_words.txt','r', encoding='utf-8') as sw:
            self.stopwords = [word.strip('\n') for word in sw]
            #print(self.stopwords)
        with open('data/stopwords/gossiping.tag','r', encoding='utf-8') as sw:
            self.stoptags = [word.strip('\n') for word in sw]

    def process_raw_data(self, path, is_dir=False, to_one_file=False, one_file_name="corpus.json"):

        data = []
        total = []
        filename = None
        count = 0

        if is_dir:
            filenames = [name for name in os.listdir(path) if not name.startswith(".")]
        else:
            filenames = [path]

        for filename in filenames:

            count +=1
            if count % 100 == 0:
                logging.info("已處理 %d 頁文章, 其中有效文章數為 %d" % (count, self.article_count))

            with open(os.path.join(path, filename),'r', encoding="utf-8") as data:
                res = self.generate_corpus(json.load(data))

                if to_one_file:
                    total += res
                else:
                    with open("data/processed/"+filename,'w', encoding='utf-8') as op:
                        op.write(json.dumps(res, indent=4, ensure_ascii=False))
                        logging.info("已處理 " + filename)
        if to_one_file:
            with open("data/processed/" + one_file_name,'w', encoding='utf-8') as op:
                op.write(json.dumps(total, indent=4, ensure_ascii=False))

    def roclean_corpus(self):
        pass

    def merge_coprus(self, path="data/processed/"):

        corpus_names = [name for name in os.listdir(path) if not name.startswith(".")]
        all_corpus = []
        for corpus_name in corpus_names:
            with open(os.path.join(path, corpus_name),'r', encoding='utf-8') as data:
                c = json.load(data)
                all_corpus += c
        with open("data/processed/all_corpus.json", 'w', encoding='utf-8') as op:
            op.write(json.dumps(all_corpus, indent=4, ensure_ascii=False))

    def load_processed_corpus(self, path="data/processed/"):

        corpus_names = [name for name in os.listdir(path)
                        if not name.startswith(".") and os.path.isfile(os.path.join("data/processed/",name))]

        logging.info("正在載入現有語料")
        for corpus_name in corpus_names:
            with open(os.path.join(path, corpus_name),'r', encoding='utf-8') as data:
                c = json.load(data)
                self.corpus += c
                logging.info("已讀入 %d 篇文章" % len(self.corpus))

        logging.info("正在抽取文章與回應")
        for article in self.corpus:
            self.titles.add(article["Title"])
            self.order_titles.append(article["Title"])
            self.order_response.append(article["Responses"])
        logging.info("文章與回應抽取完成")


    def generate_corpus(self, articles, drop_response=True, negative_tag=None, no_content=True, min_length=6):

        """
        依據需求挑選出符合語料庫需求的文章

        Args:
            - articles: 描述文章的字典，格式參見 PTT-Crawler
            - drop_response: 是否濾除回應文章
            - negative_tag: 要濾除的標籤集
            - no_content: 是否需要保存文章內容
            - min_length: 只保存長度超過 min_length 之標題
        Return:
            - coprus: 一個儲存符合需求的文章列表
        """

        if negative_tag is None:
            negative_tag = self.stoptags

        clean_article = []

        for article in articles:
            #####################濾除非結構化文章#####################
            try:
                title = article["Title"]
                clean_responses = self.clean_responses(article["Responses"])
                if len(clean_responses) == 0:
                    continue # 不需要沒有回應的文章
                article["Responses"] = clean_responses
            except Exception as e:
                #print("Wrong Format: %s" % str(e))
                continue
            ######################文章客製化選項######################
            if title in self.titles or len(title) < min_length:
                #捨去已存在語料庫的標題或過短的標題
                continue

            if drop_response:
                #捨去回應類文章與快訊文章, i.e Re: and Fw:
                if title.startswith("Re") or title.startswith("Fw"):
                    continue
            if no_content:
                article.pop("Content")
            #######################標籤抽取##########################
            tag, clean_title = self.get_tag(title) #將標題與標籤分開
            if tag in negative_tag:
                continue

            article["Tag"]   = tag
            article["Title"] = clean_title
            self.titles.add(clean_title)
            self.order_titles.append(clean_title)
            self.order_response.append(clean_responses)

            self.article_count += 1
            clean_article.append(article)

        return clean_article

    def clean_responses(self, responses, negative_user=set(), min_length=6, stopwords=None):

        """
        依照負面使用者案例、回應長度與是否包含停用詞來濾除負面的回應

        Args:
            - responses: 回應的 dictionary
            - negative_user: 要濾除該 User set 的回應
            - min_length: 濾除低於 min_length 的回應
            - stopwords: 濾除有敏感字詞的回應
        Return:
            - Responses: 已清除負面回應的字典
        """

        if stopwords is None:
            stopwords = self.stopwords

        clean_responses = []

        for response in responses:

            #self._update_users_history(response) # 更新使用者推噓文紀錄
            drop = False

            # 濾除過短與特定使用者的回應
            if response["User"] in negative_user or len(response["Content"]) < min_length:
                drop = True
            # 濾除包含停用詞的回應
            for w in stopwords:
                if w in response["Content"]:
                    drop = True
            if not drop:
                response["Content"] = response["Content"].strip()
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

        logging.info("正在輸出文章標題")
        with open('data/Titles.txt','w',encoding='utf-8') as op:
            for title in self.order_titles:
                op.write(title + "\n")
        logging.info("文章標題輸出完成")


    def print_user_info(self):
        with open('data/User_info.txt','w',encoding='utf-8') as op:
            op.write(json.dumps(self.users_info, indent=4, ensure_ascii=False))

    def print_response(self):
        logging.info("正在輸出回應內容")
        resSplit = []
        sc = 0

        for response in self.order_response:
            sc += 1
            resSplit.append(response)
            if sc % 1000 == 0:
                with open('data/processed/reply/'+str(int(sc/1000) - 1)+'.json','w',encoding='utf-8') as tr:
                    tr.write(json.dumps(resSplit, indent=4, ensure_ascii=False))
                    resSplit = []
                logging.info("已輸出 %d 篇回應" % sc)
        logging.info("回應輸出完成")

if __name__ == '__main__':
    main()
