
import jieba
import logging

from gensim import corpora, models, similarities
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfVectorizer

from corpus import PTTCorpus

def main():

    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    analyst = TfIdfAnalyst()

    # 若尚未斷詞才需運行，下列兩函式將 PTTCorpus 的文章斷詞後輸出至
    #data/processed_seged/seged_text.txt
    #analyst.load_corpus("PTTCorpus")
    #analyst.corpus_segmentation()

    analyst.load_corpus(corpus_type="SegmentedDocuments")
    analyst.tf_idf(using="gensim")

class TfIdfAnalyst(object):

    def __init__(self):

        self.corpus = None
        self._jieba_custom_setting()
        self.doc_segmented = False
        self.stopwords = set()
        self.special_marks = set()

        with open('data/stopwords/chinese_sw.txt','r',encoding='utf-8') as sw:
            for w in sw:
                self.stopwords.add(w.strip('\n'))
        with open('data/stopwords/specialMarks.txt','r',encoding='utf-8') as sm:
            for m in sm:
                self.special_marks.add(m.strip('\n'))


    def load_corpus(self, corpus_type, corpus_path="data/processed"):

        """
        讀取語料庫，為 Corpus.py 產生出的 PTT 篩選後語料，
        以及將 PTTCorpus 內容斷詞完成的 SegmentedDocuments
        """

        if corpus_type == "PTTCorpus":
            self.corpus = PTTCorpus()
            self.corpus.load_data(corpus_path,is_dir=True)

        elif corpus_type == "SegmentedDocuments":
            self.doc_segmented = True
            with open('data/processed_seged/seged_text.txt','r',encoding='utf-8') as docs:
                self.corpus = [doc.strip('\n') for doc in docs]
                print("# Documents: %d " % len(self.corpus))

    def _jieba_custom_setting(self):

        """
        jieba custom setting.
        """
        jieba.set_dictionary("jieba_dictionary/dict.txt.big")

    def corpus_segmentation(self):

        with open('data/processed_seged/seged_text.txt','w',encoding='utf-8') as op:
            for text in self.corpus.get_text():
                seged = [word for word in jieba.cut(text,cut_all=False)
                         if word not in self.stopwords
                         and word not in self.special_marks]
                op.write((" ".join(seged)+'\n'))

    def output_segmented_text(self):
        pass

    def tf_idf(self, using="gensim"):

        assert self.doc_segmented, "請先完成 PTT Corpus 的斷詞"

        if using == "sklearn":
            vectorizer = TfidfVectorizer()
            tfidf = vectorizer.fit_transform(self.corpus)
            print (tfidf.shape)

            word = vectorizer.get_feature_names()
            weight = tfidf.toarray()

            f = open("data/tf_idf.model",'w')
            for i in range(len(weight)) :
                for j in range(len(word)):
                    f.write(word[j]+":"+str(weight[i][j])+"\n")
            f.close()

        elif using == "gensim":
            corpus = [doc.split() for doc in self.corpus]
            dictionary = corpora.Dictionary(corpus)
            print(dictionary)

            corpus = [dictionary.doc2bow(doc.split()) for doc in self.corpus]
            tfidf = models.TfidfModel(corpus)
            corpus_tfidf = tfidf[corpus]
            """
            with open('data/tf_idf.model','w',encoding='utf-8') as op:
                for doc in corpus_tfidf:
                    op.write(" ".join(doc)+'\n')
            """
            lda = models.LdaModel(corpus_tfidf, id2word=dictionary, num_topics=200)
            lda.print_topics(20)

if __name__ == '__main__':
    main()
