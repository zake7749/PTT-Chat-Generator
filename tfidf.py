
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
    #analyst.corpus_segmentation(title_only=True)

    analyst.load_corpus(corpus_type="SegmentedDocuments", title_only=True)
    #analyst.tf_idf(using="gensim")
    analyst.doc2bow()

class TfIdfAnalyst(object):

    def __init__(self):

        self.corpus = None
        self._jieba_custom_setting()
        self.doc_segmented = False
        self.stopwords = set()
        self.special_marks = set()
        self.index = None

        with open('data/stopwords/chinese_sw.txt','r',encoding='utf-8') as sw:
            for w in sw:
                self.stopwords.add(w.strip('\n'))
        with open('data/stopwords/specialMarks.txt','r',encoding='utf-8') as sm:
            for m in sm:
                self.special_marks.add(m.strip('\n'))


    def load_corpus(self, corpus_type, corpus_path="data/processed", title_only=False):

        """
        讀取語料庫，為 Corpus.py 產生出的 PTT 篩選後語料，
        以及將 PTTCorpus 內容斷詞完成的 SegmentedDocuments
        """

        if title_only:
            fix = "_title_only"
        else:
            fix = "_full"

        if corpus_type == "PTTCorpus":
            self.corpus = PTTCorpus()
            self.corpus.load_data(corpus_path,is_dir=True)

        elif corpus_type == "SegmentedDocuments":
            self.doc_segmented = True
            with open('data/processed_seged/seged_text' + fix + '.txt','r',encoding='utf-8') as docs:
                self.corpus = [doc.strip('\n') for doc in docs]
                print("# Documents: %d " % len(self.corpus))

    def _jieba_custom_setting(self):

        """
        jieba custom setting.
        """
        jieba.set_dictionary("jieba_dictionary/dict.txt.big")

    def corpus_segmentation(self, title_only=False):

        if title_only:
            generator = self.corpus.get_titles()
            fix = "_title_only"
        else:
            generator = self.corpus.get_text()
            fix = "_full"

        with open("data/processed_seged/seged_text" + fix + ".txt",'w',encoding='utf-8') as op:
            for text in generator:
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
            index = similarities.MatrixSimilarity(lda[corpus_tfidf])
            #index.save('res.index')
            #lda.print_topics(20)

            while True:
                res = input("Search")
                vec_bow = dictionary.doc2bow(jieba.cut(res,cut_all=False))
                vec_lda = lda[vec_bow]
                print(vec_lda)
                sims = index[vec_lda]
                sims = sorted(enumerate(sims), key=lambda item: -item[1])
                print(sims)

    def load_sim_index(self):
            index = similarities.MatrixSimilarity.load('/tmp/deerwester.index')

    def doc2bow(self):

            while(True):
                no = input("ID: ")
                print(self.corpus[int(no)])


if __name__ == '__main__':
    main()
