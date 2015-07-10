#
#
# crawls eng.snu.ac.kr notice
#

import urllib, urllib2, requests
from bs4 import BeautifulSoup
import private

#
# parse page -> title & url & detail & id
# eg. board url: http://eng.snu.ac.kr/bbs/notice_view.php?bbsid=notice&bbsidx=%d
#
def ParsePage(url):
    articles = []
    r = requests.get(url)
    if (r.status_code != 200):
        return []
    soup = BeautifulSoup(r.content)
    trs = soup.find(id="content_body").find("form").find_all("div", class_="clear")
    for tr in trs[1:-1]:
        tds = tr.find_all("li")
        id = tds[2].find("a")["href"][22:-2]
        url = "http://eng.snu.ac.kr/bbs/notice_view.php?bbsid=notice&bbsidx=%s" % id
        title = tds[2].find("a").get_text()
        detail = tds[2].find("div").get_text()
        articles.append({"id": id,
            "url": url,
            "title": "[SNUEngineering] " + title,
            "detail": detail})
    return articles

#
# return all categories' articles
#
def getAllArticles():
    articles = []
    for url in private.urls_snueng:
        articles += ParsePage(url)
    return articles

#
###############################################################
#
# common function: checkAllasRead
#
ignored_ids = []    # these ids is already recognized so won't going to be posted
def checkAllasRead():
    global ignored_ids
    for article in getAllArticles():
        if (article['id'] not in ignored_ids):
            ignored_ids.append(article['id'])
    print '%d articles checked as read' % len(ignored_ids)

#
# common function: getNewArticle
# new articles will be automatically added to ignored_ids
#
def getNewArticles():
    global ignored_ids
    articles = []
    new_cnt = 0
    for article in getAllArticles():
        if (article['id'] not in ignored_ids):
            articles.append(article)
            ignored_ids.append(article['id'])
        
    print '[SNUEngineering] new Articles %d' % new_cnt
    return articles

#checkAllasRead()
