#
#
# crawls eng.snu.ac.kr notice
#

import urllib, urllib2, requests
from bs4 import BeautifulSoup

category_urls = ['http://eng.snu.ac.kr/bbs/notice_list.php?code_value=SN060101&user_rpp=20&b_type=',
    'http://eng.snu.ac.kr/bbs/janghak_list.php?code_value=SN060103&user_rpp=20&b_type=']

#
# parse page -> title & url & detail & id
# eg. board url: http://eng.snu.ac.kr/bbs/notice_view.php?bbsid=notice&bbsidx=%d
#
def ParsePage(url):
    articles = []
    r = session.get(url)
    if (r.status_code != 200):
        return []
    soup = BeautifulSoup(r.content)
    trs = soup.find(id="content_body").find("ol", class_="pa_t7").find_all("li")
    for tr in trs:
        id = tr.find("a")["href"][12:-2]
        url = "http://eng.snu.ac.kr/bbs/notice_view.php?bbsid=notice&bbsidx=%s" % id
        title = tr.find("a").get_text()
        detail = tr.find("div").get_text()
        articles.append({"id": id,
            "url": url,
            "title": title,
            "detail": detail})
    return articles

#
# return all categories' articles
#
def getAllArticles():
    articles = []
    for url in category_urls:
        articles += ParsePage(session, url)
    return articles

#
###############################################################
#
# common function: checkAllasRead
#
ignored_ids = []    # these ids is already recognized so won't going to be posted
def checkAllasRead():
    for article in getAllArticles():
        if (article['id'] not in ignored_ids):
            ignored_ids.append(article['id'])
    print '%d articles checked as read' % len(ignored_ids)

#
# common function: getNewArticle
# new articles will be automatically added to ignored_ids
#
def getNewArticle():
    articles = []
    new_cnt = 0
    for article in getAllArticles():
        if (article['id'] not in ignored_ids):
            articles.append(article)
            ignored_ids.append(article['id'])
        
    print 'new Articles %d' % new_cnt
    return articles
