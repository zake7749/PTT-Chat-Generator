import gensim

# 引入斷詞與停用詞的配置
from Matcher.matcher import Matcher

class Evaluator(matcher):
    """
    讀入一串推文串列，計算出當中可靠度最高的推文
    """


class ClusteringEvaluator(ResponseEvaluator):
    """
    基於聚類評比推文可靠度
    """
