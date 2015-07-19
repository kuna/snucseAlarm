#
# just load webpage from snucse

import crawler_snucse, crawler_eng, crawler_etl

def getNewArticles():
	articles = []
	try:
		# prepare
		crawler_snucse.refreshSession()
		crawler_etl.refreshSession()

		articles += crawler_snucse.getNewArticles()
		articles += crawler_eng.getNewArticles()
		articles += crawler_etl.getNewArticles()
	except:
		print "something wrong with parsing"

	return articles

def initcrawler():
    crawler_snucse.checkAllasRead()
    crawler_eng.checkAllasRead()
    crawler_etl.checkAllasRead()
