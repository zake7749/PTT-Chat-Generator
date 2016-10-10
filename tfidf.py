
import jieba

from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfVectorizer

from corpus import PTTCorpus

def main():

    analyst = TfIdfAnalyst()

    # 若尚未斷詞才需運行，下列兩函式將 PTTCorpus 的文章斷詞後輸出至
    # data/processed_seged/seged_text.txt
    # analyst.load_corpus("PTTCorpus")
    # analyst.corpus_segmentation()

    analyst.load_corpus(corpus_type="SegmentedDocuments")
    analyst.tf_idf()

class TfIdfAnalyst(object):

    def __init__(self):

        self.corpus = None
        self._jieba_custom_setting()
        self.doc_segmented = False

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
                seged = jieba.cut(text,cut_all=False)
                op.write((" ".join(jieba.cut(text, cut_all=False)))+'\n')

    def output_segmented_text(self):
        pass

    def tf_idf(self):

        assert self.doc_segmented, "請先完成 PTT Corpus 的斷詞"

        vectorizer = TfidfVectorizer()
        tfidf = vectorizer.fit_transform(self.corpus)
        print (tfidf.shape)

        word = vectorizer.get_feature_names()
        weight = tfidf.toarray()

        for i in range(len(weight)) :
            f = open("data/tf_idf.model",'w')
            for j in range(len(word)):
                f.write(word[j]+"    "+str(weight[i][j])+"\n")
            f.close()


if __name__ == '__main__':
    main()
