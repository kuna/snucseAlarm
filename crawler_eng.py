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
# pretends to be a web browser
    #user_agent = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; hu-HU; rv:1.7.8) Gecko/20050511 Firefox/1.0.4'}
    r = requests.get(url)
    if (r.status_code != 200):
        return []
    soup = BeautifulSoup(r.content)
    trs = soup.find(id="main-content").find("table").find_all("tr")
    for tr in trs[1:]:
        tds = tr.find_all("td")
        id = tds[1].find("a")["href"][6:]
        url = "http://eng.snu.ac.kr/node/%s" % id
        title = tds[1].find("a").get_text()
        detail = ""#getDetail(url)
        articles.append({"id": id,
            "url": url,
            "title": "[SNUEngineering] " + title,
            "detail": detail})
    return articles

def getDetail(url):
    r = requests.get(url)
    if (r.status_code != 200):
        return ""
    soup = BeautifulSoup(r.content)
    return soup.find(id="block-system-main").find("div", class_="postArea").html()

#
# return all categories' articles
#
def getAllArticles():
    articles = []
    for url in private.urls_snueng:
        article = ParsePage(url)
        article['detail'] = getDetail(article['url']) #lazyfill detail
        articles += article
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


if __name__=="__main__":
    print("You executed submodule directly. would you like to test your submodule?\n"\
        "(but you provide your information in private.py correctly) (y/n) >")
    if (raw_input() == "y"):
        print getNewArticles()
