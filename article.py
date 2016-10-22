class Article(object):

    """
    文章的保存結構，包含了文章標題、作者、與回文狀態 (不包含文章內容)
    """

    def __init__(self, article):

        """
        Args:
            - article: a dictionary. Load from processed json files.
        """

        self.title = article["Title"]
        self.author = article["Author"]
        self.up = article["UpVote"]
        self.down = article["DownVote"]
        self.noVote = article["NoVote"]
        self.hot = self.up + self.down + self.noVote
        self.grade = (self.up - self.down)/self.hot

        self.responses = []
        self.merge_response(article["Responses"])

    def merge_response(self, responses):

        """
        將過長的推文合併回去
        """
        cur_resp = {
            "User": responses[0]["User"],
            "Content": responses[0]["Content"],
            "Vote": responses[0]["Vote"]
        }

        for i in range(1,len(responses)-1):

            if responses[i]["User"] == cur_resp["User"]:
                cur_resp["Content"].rsrtip('\n') # 將上一篇推文的換行去除
                cur_resp["Content"] += responses[i]["Content"]
            else:
                self.responses.append(cur_resp)
                cur_resp = {
                    "User": responses[i]["User"],
                    "Content": responses[i]["Content"],
                    "Vote": responses[i]["Vote"]
                }
        self.responses.append(cur_resp)
