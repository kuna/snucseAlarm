#-*- coding: utf-8 -*-

# from private: snu_id, snu_password
import private

import urllib, urllib2, requests
from bs4 import BeautifulSoup

# customize your etl board (board list url)
etl_urls = [""]

def Login():
    session = requests.Session()
    def doLogin():
        # get response from first request
        # and send request again to get logined
        r = session.post("https://sso.snu.ac.kr/safeidentity/modules/auth_idpwd",
            data={"si_redirect_address": "",
            "si_realm": "SnuUser1",
            "_enpass_login_": "submit",
            "langKnd": "en",
            "si_id": private.snu_id,
            "si_pwd": private.snu_password,
            "btn_login.x": 0,
            "btn_login.y": 0})
        if (r.status_code != 200):
            return False
        fcs_data = {}
        login_soup = BeautifulSoup(r.content)
        for ctrl_input in login_soup.find_all("input"):
            fcs_data[ctrl_input["name"]] = ctrl_input["value"]
        r = session.post("https://sso.snu.ac.kr/nls3/fcs", data=fcs_data)
        if (r.status_code != 200):
            return False
        return True

    if (not doLogin()):
        return None
    else:
        return session

def getDetail(session, url):
    r = session.get(url)
    if (r.status_code != 200):
        return None
    soup = BeautifulSoup(r.content)
    return soup.find("div", class_="text_to_html").get_text()

def ParsePage(session, url):
    articles = []
    r = session.get(url)
    if (r.status_code != 200):
        return []
    soup = BeautifulSoup(r.content)
    trs = soup.find(id="ubboard_list_form").find_all("tr")
    for tr in trs[1:]:
        tds = tr.find_all("td")
        title = tds[1].find("a").get_text().strip()
        url = tds[1].find("a")["href"]
        detail = "none"     # lazy crawler
        id = url[url.index("bwid=")+5:]
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
    for url in etl_urls:
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
            # receive detail now
            global session
            article['detail'] = getDetail(session, article['url'])
            articles.append(article)
            ignored_ids.append(article['id'])
        
    print '[SNUETL] new Articles %d' % new_cnt
    return articles

# make default session
session = Login()

def refreshSession():
    global session
    session = Login()

def getSession():
    return session

#
##########################################################
#

def test():
    s = Login()
    if (s == None):
        print "failed to login"
    print ParsePage(s, "http://etl.snu.ac.kr/mod/ubboard/view.php?id=337196")

# login and get etl source for test
#test()
