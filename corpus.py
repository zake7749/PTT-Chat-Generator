import os
import json

from gensim import corpora
from article import Article


class Corpus(object):

    def __init__(self):
        self.corpus = []
        pass

class PTTCorpus(Corpus):

    def __init__(self):
        self.corpus = []

    def load_data(self, path, is_dir=False):

        data = []
        filename = None

        if is_dir:
            filenames = [name for name in os.listdir(path) if not name.startswith.(".")]
        else:
            filenames = [path]

        for filename in filenames:
            with open(os.path.join(path, filename),'r', encoding="utf-8") as data:
                tp = json.load(data)
                for article in tp:
                    try:
                        self.corpus.append(Article(article))
                    except:
                        print("於 %s 發生某篇文章的解析錯誤" % filename)

    def get_text(self):
        for article in self.corpus:

            title = article.title
            resp = ""
            for r in article.responses:
                resp += ' ' + r["Content"]
            yield title + resp

    def get_titles(self):
        for article in self.corpus:
            yield article.title
