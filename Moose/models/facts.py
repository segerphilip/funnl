from article import Article

class Facts(object):
    def __init__(self, articles):
        if type(articles) != type(list()):
            raise Exception("Invalid type for articles")

        self.articles = articles
