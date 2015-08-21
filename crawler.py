#
# just load webpage from snucse

import crawler_snucse, crawler_eng, crawler_etl

session_objs = [crawler_snucse, crawler_etl]
article_objs = [crawler_snucse, crawler_eng, crawler_etl]

def getNewArticles():
    articles = []

    for obj in session_objs:
        try:
            crawler_snucse.refreshSession()
            crawler_etl.refreshSession()
        except:
            print "something wrong with login(session)"

    for obj in article_objs:
        try:
            articles += obj.getNewArticles()
        except:
            print "something wrong with parsing"

	return articles

def initcrawler():
    for obj in article_objs:
        try:
            obj.checkAllasRead()
        except:
            print "initalizing(checkAllasRead) failed.", obj
