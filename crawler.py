#
# just load webpage from snucse

import crawler_snucse, crawler_eng, crawler_etl

def getNewArticles():
    # prepare
    crawler_snucse.refreshSession()

    articles = []
    articles += crawler_snucse.getNewArticles()
    articles += crawler_eng.getNewArticles()
    articles += crawler_etl.getNewArticles()
    return articles

def initcrawler():
    crawler_snucse.checkAllasRead()
    crawler_eng.checkAllasRead()
    crawler_etl.checkAllasRead()
