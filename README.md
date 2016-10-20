# PTT Text Mining

本專案的目的在實作一個推文產生器，由使用者輸入一個隨機標題，即能回覆一個恰當的推文，目前仍在進行中 d(`･∀･)b

## 類別說明

* [PTT-Crawler](https://github.com/zake7749/PTT-Crawler): 用於爬取 PTT 頁面的原始文章
* `filter.py`: 用於過濾 PTT-Crawler 爬取下來的文章，如濾除某些標籤或某些使用者的文章，或是濾除內容重覆的文章等
* `article.py`: 儲存 PTT 文章的結構，會將分段式的回覆合併起來
* `corpus.py`: 保存 Article 的結構，可遍歷文章的標題、內容
* `match.py`: 調用不同的 Matcher 實驗
* `Matcher`: 用於文本相似度的比對，將使用者的輸入與 Corpus 裡所有標題比較，回傳最相似的標題與索引
  * `FuzzyMatcher`: 基於 Levenshtein Distance 比對短語相似度
  * `VectorMatcher`: 基於 sentence2vec 比對短語相似度 TODO!
  * `KeywordMatcher`: 基於 tf/idf 比對短語相似度 TODO!

## 套件需求

* sklearn : 訓練 tfidf、文本特徵分類
* jieba : 中文隱性馬可夫模型斷詞器
* Taiba : 繁體中文 CRF 斷詞器 （預設使用 Taiba）
* gensim : 使用詞袋、tfidf、word2vec
* fuzzywuzzy : 模糊字串比對
  * python-Levenshtein : 用於優化 fuzzywuzzy 計算速度的套件包
* sentence2vec(optional)

## Data
* raw: 儲存PTT-Crawler爬取的原始資料
* processed: 儲存已經篩選過的文章（如濾除特定標籤、使用者）
  * reply: 儲存文章回應，每 1000 筆為一個檔案
* processed_seged: 儲存文章或回應的斷詞結果
* stopwords: 儲存常用中文停用詞、PTT 停用詞、負面標籤
* User_info: 基於 raw 的使用者推噓文紀錄
* Titles.txt: 存放篩選後文章的標題

## 實驗簡述

1. 使用 PTT-Crawler 爬取文章後放置於 "data/raw/"
2. 使用 filter.py 從原始資料裡挑選出需要的資料
3. 使用 match.py 測試匹配結果
