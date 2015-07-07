#

import crawler
import mail
import datetime
import sys
import time

def timemilisec():
    return int(round(time.time() * 1000))

def loop():
    # continously loop to find new message
    # scan per 60min
    current_time = timemilisec()
    while True:
        new_time = timemilisec()
        if (new_time - current_time > 1000*60*60):
            articles = crawler.getNewArticles()
            if (len(articles) > 0):
                print 'new articles found: %d' % len(articles)
                mail.emailArticles(articles)
        time.sleep(10)

def initcrawler():
    crawler.initcrawler()

def main():
    print 'starting mailer ...'
    print 'to exit ^C'
    try:
        initcrawler()
        print 'initalize finished.'
        loop()
    except KeyboardInterrupt:
        print 'bye (by ^C)'
        exit()
    print 'exit program (by exiting loop func)'

if __name__ == "__main__":
    main()
