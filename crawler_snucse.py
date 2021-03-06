#-*- coding: utf-8 -*-
# just load webpage from snucse

# from private: snucse_id, snucse_password, categories
import private

import urllib, urllib2, requests
from bs4 import BeautifulSoup

# change console locale
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#
# login function
#
def Login():
    session = requests.Session()
    def doLogin():
        r = session.post("https://www.snucse.org/Authentication/Login.aspx",
            data={"login_type": "member_login",
                "referrer": "/",
                "redirect_mode": "none",
                "member_account": private.snucse_id,
                "member_password": private.snucse_password,
                "secure": "on"})
        if (r.status_code == 200):
            return True
        else:
            return False

    # login with session
    if (not doLogin()):
        return None
    else:
        return session
    #r = session.get("http://www.snucse.org/")
    #print session.cookies.get_dict()

def getDetail(session, url):
    r = session.get(url)
    if (r.status_code != 200):
        return None
    soup = BeautifulSoup(r.content)
    element_article = soup.find(id="ArticleContent")
    if (element_article == None):
        return "cannot find detail"
    else:
        return element_article.get_text()

#
# parse page -> title & url & detail
#
def ParsePage(session, url):
    articles = []
    r = session.get(url)
    if (r.status_code != 200):
        return []
    soup = BeautifulSoup(r.content)
    trs = soup.find(id="Panorama").find_all("tr")
    for tr in trs[1:]:
        tds = tr.find_all("td")
        if (tds[2].find("a") == None):
            # it's removed article so ignore and continue
            continue
        url = tds[2].find("a")["href"]
        url_absolute = url.replace("../", "http://www.snucse.org/")
        title = tds[2].get_text()
        articles.append({"id": url.replace("../", ""),
            "url": url_absolute,
            "title": "[SNUCSE] " + title,
            "detail": "none"})
    return articles

#
# return all categories' articles
#
def getAllArticles():
    articles = []
    for url in private.urls_snucse:
        articles += ParsePage(session, url)
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
    #ignored_ids = ignored_ids[:-1] # for test: omit 1 id purposly

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
            global session
            article['detail'] = getDetail(session, article['url'])
            articles.append(article)
            ignored_ids.append(article['id'])
        
    print '[SNUCSE] new Articles %d' % new_cnt
    return articles

# make default session
session = Login()

def refreshSession():
    global session
    session = Login()

def getSession():
    return session



if __name__=="__main__":
    print("You executed submodule directly. would you like to test your submodule?\n"\
        "(but you provide your information in private.py correctly) (y/n) >")
    if (raw_input() == "y"):
        refreshSession()
        print getNewArticles()
