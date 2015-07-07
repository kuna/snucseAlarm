#
# just load webpage from snucse

import crawler_snucse, crawler_eng

def getNewArticles():
    # prepare
    crawler_snucse.refreshSession()

    articles = []
    articles += crawler_snucse.getNewArticles()
    articles += crawler_eng.getNewArticles()
    return articles

def initcrawler():
    crawler_snucse.checkAllasRead()
    crawler_eng.checkAllasRead()
