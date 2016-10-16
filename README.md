# PTT Text Mining

本專案的目的在實作一個推文產生器，由使用者輸入一個隨機標題，即能回覆一個恰當的推文，目前仍在進行中 d(`･∀･)b

## 類別說明

* `[PTT-Crawler](https://github.com/zake7749/PTT-Crawler)`: 用於爬取 PTT 頁面的原始文章
* `filter.py`: 用於過濾 PTT-Crawler 爬取下來的文章，如濾除某些標籤或某些使用者的文章，或是濾除內容重覆的文章等
* `article.py`:儲存 PTT 文章的結構，會將分段式的回覆合併起來
* `corpus.py`:保存 Article 的結構，可遍歷文章的標題、內容
* `match.py`:調用不同的 Matcher 實驗 
* `Matcher`:用於文本相似度的比對，將使用者的輸入與 Corpus 裡所有標題比較，回傳最相似的標題與索引
  * `FuzzyMatcher`: 基於 Levenshtein Distance 比對短語相似度
  * `VectorMatcher`: 基於 sentence2vec 比對短語相似度 TODO!
  * `KeywordMatcher`: 基於 tf/idf 比對短語相似度 TODO!
